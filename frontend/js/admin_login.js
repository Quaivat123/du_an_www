const API_BASE_URL = window.location.origin;
const TOKEN_EXPIRATION_TIME = 3 * 60 * 1000; // 3 phút (tính bằng milliseconds)
let tokenTimeoutId = null;

// === Event Listeners ===
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const logoutBtn = document.getElementById('logout-button');

    if (loginForm) loginForm.addEventListener('submit', handleLogin);
    if (logoutBtn) logoutBtn.addEventListener('click', handleLogout);

    // Kiểm tra token hết hạn khi load trang
    checkTokenExpiration();
});

// === Check Token Expiration (dựa trên timestamp) ===
function checkTokenExpiration() {
    const token = localStorage.getItem('accessToken');
    const loginTimestamp = localStorage.getItem('loginTimestamp');

    if (!token || !loginTimestamp) return;

    const currentTime = Date.now();
    const elapsedTime = currentTime - parseInt(loginTimestamp);

    // Nếu hết hạn, logout ngay
    if (elapsedTime > TOKEN_EXPIRATION_TIME) {
        alert('Phiên đăng nhập đã hết hạn! Vui lòng đăng nhập lại.');
        handleLogout();
        return;
    }

    // Nếu vẫn còn hạn, set timer cho thời gian còn lại
    const remainingTime = TOKEN_EXPIRATION_TIME - elapsedTime;
    if (tokenTimeoutId) clearTimeout(tokenTimeoutId);
    tokenTimeoutId = setTimeout(() => {
        alert('Phiên đăng nhập đã hết hạn! Vui lòng đăng nhập lại.');
        handleLogout();
    }, remainingTime);
}

// === Set Token Expiration Timer ===
function setTokenExpiration() {
    // Lưu timestamp lúc đăng nhập (chỉ lưu lần đầu)
    if (!localStorage.getItem('loginTimestamp')) {
        localStorage.setItem('loginTimestamp', Date.now().toString());
    }

    // Xóa timer cũ nếu có
    if (tokenTimeoutId) clearTimeout(tokenTimeoutId);

    // Đặt timer mới - hết hạn sau 3 phút
    tokenTimeoutId = setTimeout(() => {
        alert('Phiên đăng nhập đã hết hạn! Vui lòng đăng nhập lại.');
        handleLogout();
    }, TOKEN_EXPIRATION_TIME);
}

// === Login Handler ===
async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const messageEl = document.getElementById('login-message');

    try {
        const response = await fetch(`${API_BASE_URL}/admin/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('accessToken', data.access_token);
            messageEl.textContent = "Đăng nhập thành công!";
            messageEl.style.color = 'green';

            // Ẩn form login và hiện UI quản trị
            showAdminUI();

            // Bắt đầu bộ đếm thời gian hết hạn token
            setTokenExpiration();

            // Tải danh sách contacts
            setTimeout(() => {
                if (typeof loadContacts === 'function') {
                    loadContacts();
                }
            }, 100);
        } else {
            messageEl.textContent = data.detail || "Đăng nhập thất bại.";
            messageEl.style.color = 'red';
        }
    } catch (error) {
        messageEl.textContent = "Lỗi kết nối server.";
        messageEl.style.color = 'red';
        console.error('Login error:', error);
    }
}

// === Logout Handler ===
function handleLogout() {
    // Xóa timer
    if (tokenTimeoutId) clearTimeout(tokenTimeoutId);

    localStorage.removeItem('accessToken');
    localStorage.removeItem('loginTimestamp');
    showLoginUI();
}

// === Auth Headers (used by other files) ===
function getAuthHeaders() {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        showLoginUI();
        return null;
    }
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
}

// === UI Toggle Functions ===
function showAdminUI() {
    document.getElementById('login-container').style.display = 'none';
    document.getElementById('contacts-container').style.display = 'block';
}

function showLoginUI() {
    document.getElementById('login-container').style.display = 'block';
    document.getElementById('contacts-container').style.display = 'none';
}

