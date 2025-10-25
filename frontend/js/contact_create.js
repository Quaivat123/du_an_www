// file: /static/js/contact-create.js

// ***************************************************************
// THIẾT LẬP CẤU HÌNH API
// ***************************************************************
// Thay đổi giá trị này thành URL cơ sở của backend FastAPI của bạn
const API_BASE_URL = 'http://127.0.0.1:8000';
// Hoặc 'http://localhost:8000' nếu bạn đang chạy FastAPI trên cổng 8000
// Khi deploy, hãy thay thế bằng domain thực tế.

// ***************************************************************
// HÀM XỬ LÝ GỬI DỮ LIỆU ĐẾN API
// ***************************************************************
async function submitCreateContact(formEl) {
    const formData = new FormData(formEl);

    // Thu thập dữ liệu, đảm bảo các key khớp với schemas.ContactCreate (name, email, phone_number, message)
    const newContact = {
        name: formData.get('name'),
        email: formData.get('email'),
        phone_number: formData.get('phone_number'),
        message: formData.get('message')
    };

    // Endpoint: Khớp với router FastAPI (prefix="/contact", path="/") -> /contact/
    const endpoint = `${API_BASE_URL}/contact/`;

    try {
        const response = await fetch(endpoint, {
            method: 'POST', // Phương thức tạo mới
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newContact) // Gửi dữ liệu dưới dạng JSON
        });

        // Kiểm tra status code 201 (HTTP_201_CREATED) từ FastAPI
        if (response.status === 201) {
            const data = await response.json();
            console.log('Contact đã được tạo thành công:', data);

            alert('Yêu cầu tư vấn của bạn đã được gửi thành công! Chúng tôi sẽ liên hệ lại sớm nhất.');
            formEl.reset(); // Xóa form sau khi gửi thành công
            return true;
        } else {
            // Xử lý lỗi từ server (ví dụ: lỗi validate 422, hoặc lỗi server 500)
            const errorData = await response.json();
            console.error('Lỗi API:', response.status, errorData);
            let errorMessage = "Đã xảy ra lỗi khi gửi yêu cầu.";
            if (response.status === 422) {
                // Xử lý lỗi validate từ FastAPI (Unprocessable Entity)
                errorMessage += "\nVui lòng kiểm tra lại thông tin bạn đã nhập.";
            } else if (errorData.detail) {
                errorMessage += `\nChi tiết: ${errorData.detail}`;
            }
            alert(`Gửi yêu cầu thất bại! ${errorMessage}`);
            return false;
        }
    } catch (error) {
        alert('Lỗi kết nối mạng! Vui lòng kiểm tra kết nối internet hoặc thử lại sau.');
        console.error('Lỗi kết nối:', error);
        return false;
    }
}


// ***************************************************************
// KHỞI TẠO VÀ LẮNG NGHE SỰ KIỆN SUBMIT
// ***************************************************************

document.addEventListener('DOMContentLoaded', function() {
    // 1. Lấy phần tử form trong Contact Section
    const contactForm = document.querySelector('#contact form');

    if (contactForm) {
        // 2. Lắng nghe sự kiện 'submit'
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault(); // Ngăn form submit mặc định (tải lại trang)

            // 3. Gọi hàm xử lý gửi dữ liệu
            await submitCreateContact(e.target);
        });
    } else {
        console.warn("Không tìm thấy form liên hệ. Chức năng gửi dữ liệu sẽ không hoạt động.");
    }
});