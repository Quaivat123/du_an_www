// === Edit Contact Modal ===
let editingContact = null;

function showEditContactForm(contact) {
    editingContact = contact;

    const formHtml = `
    <div id="edit-contact-modal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999] p-4 backdrop-blur-sm">
        <form id="edit-contact-form" class="bg-white p-8 md:p-10 rounded-xl shadow-2xl w-full max-w-lg transform transition-all duration-300 scale-100 opacity-100">
            <h3 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-3 border-orange-200">
                Chỉnh sửa Liên hệ
            </h3>

            <div class="mb-4">
                <label class="block text-lg font-medium mb-1 text-gray-700">Tên:</label>
                <input type="text" name="name" value="${contact.name || ''}" required
                       class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-blue text-gray-800 transition">
            </div>

            <div class="mb-4">
                <label class="block text-lg font-medium mb-1 text-gray-700">Email:</label>
                <input type="email" name="email" value="${contact.email || ''}" required
                       class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-blue text-gray-800 transition">
            </div>

            <div class="mb-4">
                <label class="block text-lg font-medium mb-1 text-gray-700">Số điện thoại:</label>
                <input type="text" name="phone_number" value="${contact.phone_number || ''}" required
                       class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-blue text-gray-800 transition">
            </div>

            <div class="mb-6">
                <label class="block text-lg font-medium mb-1 text-gray-700">Nội dung:</label>
                <textarea name="message" rows="4" required
                          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-blue text-gray-800 transition">${contact.message || contact.content || ''}</textarea>
            </div>

            <div class="flex justify-end space-x-4">
                <button type="button" id="cancel-edit-btn"
                        class="bg-gray-400 hover:bg-gray-500 text-white font-semibold py-2 px-6 rounded-full shadow-md transition-all duration-300 transform hover:scale-[1.05]">
                    Hủy
                </button>
                <button type="submit"
                        class="bg-[#E76F51] hover:bg-[#F4A261] text-white font-semibold py-2 px-6 rounded-full shadow-lg transition-all duration-300 transform hover:scale-[1.05]">
                    Lưu thay đổi
                </button>
            </div>
        </form>
    </div>`;

    document.body.insertAdjacentHTML('beforeend', formHtml);

    // Event Listeners
    document.getElementById('edit-contact-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await submitEditContact(contact.id, e.target);
    });
    document.getElementById('cancel-edit-btn').onclick = closeEditContactForm;
}

// === Close Modal ===
function closeEditContactForm() {
    const modal = document.getElementById('edit-contact-modal');
    if (modal) modal.remove();
    editingContact = null;
}

// === Submit Edit Contact ===
async function submitEditContact(contactId, formEl) {
    const headers = getAuthHeaders();
    if (!headers) return;

    const formData = new FormData(formEl);
    const updatedContact = {
        name: formData.get('name'),
        email: formData.get('email'),
        phone_number: formData.get('phone_number'),
        message: formData.get('message')
    };

    try {
        const response = await fetch(`${API_BASE_URL}/admin/contacts/${contactId}`, {
            method: 'PUT',
            headers: headers,
            body: JSON.stringify(updatedContact)
        });

        if (response.ok) {
            alert('Cập nhật thành công!');
            closeEditContactForm();
            if (typeof loadContacts === 'function') loadContacts();
        } else {
            const error = await response.json();
            console.error('Lỗi cập nhật:', error);
            alert('Cập nhật thất bại! - Số điện thoại không đúng định dạng!');
        }
    } catch (error) {
        console.error('Lỗi kết nối:', error);
        alert('Lỗi kết nối khi cập nhật!');
    }
}

// === Export to Global Scope ===
window.showEditContactForm = showEditContactForm;
