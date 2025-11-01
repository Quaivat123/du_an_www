// === Delete Contact Function ===
async function deleteContact(contactId) {
    if (!confirm(`Bạn có chắc chắn muốn xóa liên hệ ID ${contactId} không?`)) return;

    const headers = getAuthHeaders();
    if (!headers) return;

    try {
        const response = await fetch(`${API_BASE_URL}/admin/contacts/${contactId}`, {
            method: 'DELETE',
            headers: headers
        });

        if (response.ok) {
            alert("Xóa liên hệ thành công!");
            if (typeof loadContacts === 'function') loadContacts();
        } else {
            const error = await response.json();
            console.error('Lỗi khi xóa:', error);
            alert("Xóa thất bại!");
        }
    } catch (error) {
        console.error('Lỗi kết nối:', error);
        alert("Lỗi kết nối server!");
    }
}

// === Export to Global Scope ===
window.deleteContact = deleteContact;
