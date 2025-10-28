// === Load and Display Contacts ===
async function loadContacts() {
    const headers = getAuthHeaders();
    if (!headers) return;

    try {
        const response = await fetch(`${API_BASE_URL}/admin/contacts`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const contacts = await response.json();
            displayContacts(contacts);
        } else {
            console.error('Lỗi khi tải danh sách liên hệ');
            alert('Không thể tải danh sách liên hệ!');
        }
    } catch (error) {
        console.error('Lỗi kết nối:', error);
        alert('Lỗi kết nối server!');
    }
}

// === Display Contacts in Table ===
function displayContacts(contacts) {
    const tbody = document.getElementById('contacts-tbody');
    if (!tbody) return;

    if (!contacts || contacts.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4 text-gray-500">Không có liên hệ nào</td></tr>';
        return;
    }

    tbody.innerHTML = contacts.map(contact => `
        <tr class="hover:bg-yellow-50 transition-colors">
            <td class="py-3 px-4">${contact.id}</td>
            <td class="py-3 px-4">${contact.name || 'N/A'}</td>
            <td class="py-3 px-4">${contact.email || 'N/A'}</td>
            <td class="py-3 px-4">${contact.phone_number || 'N/A'}</td>
            <td class="py-3 px-4 max-w-xs truncate" title="${contact.message || contact.content || 'N/A'}">
                ${contact.message || contact.content || 'N/A'}
            </td>
            <td class="py-3 px-4">${formatDate(contact.created_at)}</td>
            <td class="py-3 px-4 space-x-2">
                <button onclick="showEditContactForm(${JSON.stringify(contact).replace(/"/g, '&quot;')})"
                        class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-1 px-3 rounded shadow-md transition-all">
                    Sửa
                </button>
                <button onclick="deleteContact(${contact.id})"
                        class="btn-delete text-white font-semibold py-1 px-3 rounded shadow-md transition-all">
                    Xóa
                </button>
            </td>
        </tr>
    `).join('');
}

// === Format Date Helper ===
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    try {
        const date = new Date(dateString);
        return date.toLocaleString('vi-VN');
    } catch (error) {
        return dateString;
    }
}

// === Export to Global Scope ===
window.loadContacts = loadContacts;
