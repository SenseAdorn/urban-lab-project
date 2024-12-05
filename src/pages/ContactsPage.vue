<template>
  <div class="contacts-page-container">
    <h1>Contacts Management</h1>

    <!-- Filters Panel -->
    <div class="filters-panel">
      <div class="filters-header">
        <h2>Filters</h2>
        <button @click="toggleFilters" class="toggle-button">
          {{ showFilters ? 'Hide Filters' : 'Show Filters' }}
        </button>
      </div>
      <transition name="fade">
        <div v-if="showFilters" class="filters-body">
          <div class="filters-grid">
            <div class="filter-item">
              <label>ID</label>
              <input type="number" v-model="filters.id" />
            </div>
            <div class="filter-item">
              <label>First Name</label>
              <input type="text" v-model="filters.first_name" />
            </div>
            <div class="filter-item">
              <label>Last Name</label>
              <input type="text" v-model="filters.last_name" />
            </div>
            <div class="filter-item">
              <label>Email</label>
              <input type="text" v-model="filters.email" />
            </div>
            <div class="filter-item">
              <label>Phone</label>
              <input type="text" v-model="filters.phone" />
            </div>
            <div class="filter-item">
              <label>Role</label>
              <select v-model="filters.role_name">
                <option value="">All</option>
                <option v-for="role in roles" :key="role.id" :value="role.role_name">
                  {{ role.role_name }}
                </option>
              </select>
            </div>
            <div class="filter-item">
              <label>Organization</label>
              <input type="text" v-model="filters.organization" />
            </div>
            <div class="filter-item">
              <label>City</label>
              <input type="text" v-model="filters.city" />
            </div>
            <div class="filter-item">
              <label>Country</label>
              <input type="text" v-model="filters.country" />
            </div>
          </div>
          <div class="filters-actions">
            <button class="apply-button" @click="applyFilters">Apply</button>
            <button class="reset-button" @click="resetFilters">Reset</button>
          </div>
        </div>
      </transition>
    </div>

    <!-- Table and Pagination -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Role</th>
            <th>Organization</th>
            <th>City</th>
            <th>Country</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="contact in paginatedFilteredContacts" :key="contact.id">
            <td>{{ contact.id }}</td>
            <td>{{ contact.first_name }}</td>
            <td>{{ contact.last_name }}</td>
            <td>{{ contact.email }}</td>
            <td>{{ contact.phone }}</td>
            <td>{{ contact.role_name }}</td>
            <td>{{ contact.organization }}</td>
            <td>{{ contact.city }}</td>
            <td>{{ contact.country }}</td>
            <td class="actions-cell">
              <button class="icon-button edit" @click="editContact(contact)" title="Edit">✏️</button>
              <button class="icon-button delete" @click="deleteContact(contact.id)" title="Delete">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination">
      <button class="page-button" :disabled="currentPage === 1" @click="prevPage">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button class="page-button" :disabled="currentPage === totalPages" @click="nextPage">Next</button>
    </div>

    <!-- Edit Contact Modal -->
    <div v-if="editingContact" class="modal-overlay" @click.self="cancelEdit">
      <div class="modal-content">
        <h2>Edit Contact</h2>
        <form @submit.prevent="saveContact" class="modal-form">
          <label>First Name:</label>
          <input type="text" v-model="editingContact.first_name" required />
          <label>Last Name:</label>
          <input type="text" v-model="editingContact.last_name" required />
          <label>Email:</label>
          <input type="email" v-model="editingContact.email" required />
          <label>Phone:</label>
          <input type="text" v-model="editingContact.phone" />
          <label>Role:</label>
          <select v-model="editingContact.role_name">
            <option v-for="role in roles" :key="role.id" :value="role.role_name">
              {{ role.role_name }}
            </option>
          </select>
          <label>Organization:</label>
          <input type="text" v-model="editingContact.organization" />
          <label>City:</label>
          <input type="text" v-model="editingContact.city" />
          <label>Country:</label>
          <input type="text" v-model="editingContact.country" />
          <div class="modal-actions">
            <button type="submit" class="save-button">Save</button>
            <button type="button" class="cancel-button" @click="cancelEdit">Cancel</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      contacts: [],
      roles: [],
      filters: {
        id: '',
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        role_name: '',
        organization: '',
        city: '',
        country: '',
      },
      currentPage: 1,
      pageSize: 5,
      filteredContacts: [],
      editingContact: null,
      showFilters: true
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredContacts.length / this.pageSize);
    },
    paginatedFilteredContacts() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredContacts.slice(start, end);
    },
  },
  methods: {
    async fetchContacts() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/contacts/');
        this.contacts = response.data;
        this.filteredContacts = this.contacts;
      } catch (error) {
        console.error('Failed to fetch contacts:', error);
      }
    },
    async fetchRoles() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/roles/');
        this.roles = response.data;
      } catch (error) {
        console.error('Failed to fetch roles:', error);
      }
    },
    applyFilters() {
      this.filteredContacts = this.contacts.filter(contact => {
        return (
          (this.filters.id === '' || contact.id === Number(this.filters.id)) &&
          (this.filters.first_name === '' || contact.first_name.toLowerCase().includes(this.filters.first_name.toLowerCase())) &&
          (this.filters.last_name === '' || contact.last_name.toLowerCase().includes(this.filters.last_name.toLowerCase())) &&
          (this.filters.email === '' || contact.email.toLowerCase().includes(this.filters.email.toLowerCase())) &&
          (this.filters.phone === '' || contact.phone.includes(this.filters.phone)) &&
          (this.filters.role_name === '' || contact.role_name.toLowerCase() === this.filters.role_name.toLowerCase()) &&
          (this.filters.organization === '' || contact.organization.toLowerCase().includes(this.filters.organization.toLowerCase())) &&
          (this.filters.city === '' || contact.city.toLowerCase().includes(this.filters.city.toLowerCase())) &&
          (this.filters.country === '' || contact.country.toLowerCase().includes(this.filters.country.toLowerCase()))
        );
      });
      this.currentPage = 1;
    },
    resetFilters() {
      for (let key in this.filters) {
        this.filters[key] = '';
      }
      this.applyFilters();
    },
    toggleFilters() {
      this.showFilters = !this.showFilters;
    },
    async deleteContact(id) {
      if (confirm('Are you sure you want to delete this contact?')) {
        try {
          await axios.delete(`http://127.0.0.1:5000/contacts/${id}`);
          this.fetchContacts();
        } catch (error) {
          console.error('Failed to delete contact:', error);
        }
      }
    },
    editContact(contact) {
      this.editingContact = { ...contact };
    },
    async saveContact() {
      try {
        await axios.put(`http://127.0.0.1:5000/contacts/${this.editingContact.id}`, this.editingContact);
        this.editingContact = null;
        this.fetchContacts();
      } catch (error) {
        console.error('Failed to save contact:', error);
      }
    },
    cancelEdit() {
      this.editingContact = null;
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
  },
  mounted() {
    this.fetchContacts();
    this.fetchRoles();
  },
};
</script>

<style scoped>
.contacts-page-container {
  max-width: 1200px;
  margin: 100px auto 20px auto;
  padding: 20px;
  background-color: #f7f9fa;
  border-radius: 8px;
  box-sizing: border-box;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.contacts-page-container h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
  font-size: 28px;
}

/* Filters Panel */
.filters-panel {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 20px;
  margin-bottom: 30px;
  transition: height 0.3s ease;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filters-header h2 {
  font-size: 20px;
  color: #34495e;
  margin: 0;
}

.toggle-button {
  background-color: #34495e;
  color: #ecf0f1;
  border: none;
  border-radius:4px;
  padding: 6px 12px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.toggle-button:hover {
  background-color: #2c3e50;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.filters-body {
  margin-top: 20px;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

.filter-item {
  display: flex;
  flex-direction: column;
}

.filter-item label {
  margin-bottom: 5px;
  font-weight: bold;
  color: #34495e;
  font-size: 14px;
}

.filter-item input, .filter-item select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius:4px;
  font-size: 14px;
}

.filter-item input:focus, .filter-item select:focus {
  border-color: #42b983;
  outline: none;
}

.filters-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.apply-button, .reset-button {
  border: none;
  border-radius:4px;
  padding: 8px 12px;
  cursor: pointer;
  font-weight: bold;
  color: #fff;
}

.apply-button {
  background-color: #42b983;
}
.apply-button:hover {
  background-color: #36a778;
}

.reset-button {
  background-color: #7f8c8d;
}
.reset-button:hover {
  background-color: #5f6f6f;
}

/* Table Container */
.table-container {
  overflow-x: auto;
  background-color: #fff;
  border-radius:8px;
  box-shadow:0 2px 4px rgba(0,0,0,0.1);
  padding:20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  overflow: hidden;
}

table th, table td {
  padding: 12px;
  text-align: center;
  white-space: nowrap;
  font-size:14px;
}

table th {
  background-color: #34495e;
  color: #ecf0f1;
  font-weight: bold;
}

table tr:nth-child(even) {
  background-color: #f9f9f9;
}

table tr:hover {
  background-color: #f1f1f1;
}

.actions-cell {
  display: flex;
  justify-content: center;
  gap: 5px;
}

.icon-button {
  border: none;
  background: none;
  cursor: pointer;
  font-size: 16px;
}

.icon-button.edit:hover {
  color: #42b983;
}

.icon-button.delete:hover {
  color: #e74c3c;
}

/* Pagination */
.pagination {
  margin-top: 20px;
  text-align: center;
  font-family: Arial, sans-serif;
  display: flex;
  justify-content: center;
  gap: 20px;
  align-items: center;
}

.page-button {
  background-color: #34495e;
  color: #ecf0f1;
  border: none;
  border-radius:4px;
  padding:6px 12px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.page-button:disabled {
  background-color: #7f8c8d;
  cursor: not-allowed;
}

.page-button:hover:enabled {
  background-color: #2c3e50;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top:0; left:0; width:100%; height:100%;
  background-color: rgba(0,0,0,0.5);
  display:flex; justify-content:center; align-items:center;
  z-index:2000;
}

.modal-content {
  background-color:#fff;
  padding:30px;
  border-radius:8px;
  max-width:400px;
  width:100%;
  box-sizing:border-box;
  position:relative;
}

.modal-content h2 {
  text-align:center;
  margin-bottom:20px;
  color:#2c3e50;
}

.modal-form {
  display:flex;
  flex-direction:column;
  gap:10px;
}

.modal-form label {
  font-weight:bold;
  margin-bottom:4px;
  color:#34495e;
}

.modal-form input, .modal-form select {
  padding:8px;
  border:1px solid #ccc;
  border-radius:4px;
}

.modal-form input:focus, .modal-form select:focus {
  border-color:#42b983;
  outline:none;
  box-shadow:0 0 2px rgba(66,185,131,0.5);
}

.modal-actions {
  display:flex;
  justify-content:flex-end;
  gap:10px;
  margin-top:20px;
}

.save-button, .cancel-button {
  border:none;
  border-radius:4px;
  padding:8px 12px;
  cursor:pointer;
  font-weight:bold;
  color:#fff;
}

.save-button {
  background-color:#42b983;
}
.save-button:hover {
  background-color:#36a778;
}

.cancel-button {
  background-color:#7f8c8d;
}
.cancel-button:hover {
  background-color:#5f6f6f;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .filters-grid {
    grid-template-columns: 1fr;
  }

  table th, table td {
    font-size: 12px;
    padding: 8px;
  }

  .page-button, .toggle-button {
    font-size: 12px;
    padding: 5px 10px;
  }

  .filter-item label {
    font-size:12px;
  }
}
</style>
