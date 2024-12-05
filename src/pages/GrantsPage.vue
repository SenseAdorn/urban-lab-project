<template>
  <div class="grants-page-container">
    <h1>Grants Management</h1>

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
              <label>Grant Name</label>
              <input type="text" v-model="filters.grant_name" placeholder="Search by name" />
            </div>
            <div class="filter-item">
              <label>Start Date</label>
              <input type="date" v-model="filters.start_date" />
            </div>
            <div class="filter-item">
              <label>End Date</label>
              <input type="date" v-model="filters.end_date" />
            </div>
            <div class="filter-item">
              <label>Frequency</label>
              <select v-model="filters.frequency">
                <option value="">All</option>
                <option value="One-time">One-time</option>
                <option value="Daily">Daily</option>
                <option value="Weekly">Weekly</option>
                <option value="Monthly">Monthly</option>
                <option value="Quarterly">Quarterly</option>
                <option value="Annually">Annually</option>
              </select>
            </div>
          </div>
          <div class="filters-actions">
            <button class="apply-button" @click="applyFilters">Apply</button>
            <button class="reset-button" @click="resetFilters">Reset</button>
          </div>
        </div>
      </transition>
    </div>

    <!-- Grants Table -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Grant Name</th>
            <th>Purpose</th>
            <th>Amount</th>
            <th>Frequency</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="grant in paginatedFilteredGrants" :key="grant.id">
            <td>{{ grant.grant_name }}</td>
            <td>{{ grant.purpose }}</td>
            <td>{{ grant.amount }}</td>
            <td>{{ grant.frequency }}</td>
            <td>{{ formatDate(grant.start_date) }}</td>
            <td>{{ grant.end_date ? formatDate(grant.end_date) : 'N/A' }}</td>
            <td class="actions-cell">
              <button class="icon-button edit" @click="editGrant(grant)" title="Edit">✏️</button>
              <button class="icon-button delete" @click="deleteGrant(grant.id)" title="Delete">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination Controls -->
    <div class="pagination">
      <button class="page-button" :disabled="currentPage === 1" @click="prevPage">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button class="page-button" :disabled="currentPage === totalPages" @click="nextPage">Next</button>
    </div>

    <!-- Edit Grant Modal -->
    <div v-if="editingGrant" class="modal-overlay" @click.self="cancelEdit">
      <div class="modal-content">
        <h2>{{ editingGrant.id ? 'Edit Grant' : 'Add Grant' }}</h2>
        <form @submit.prevent="saveGrant" class="modal-form">
          <label>Grant Name:</label>
          <input type="text" v-model="editingGrant.grant_name" required />
          
          <label>Purpose:</label>
          <textarea v-model="editingGrant.purpose" required></textarea>
          
          <label>Amount:</label>
          <input type="number" v-model="editingGrant.amount" required />

          <label>Frequency:</label>
          <select v-model="editingGrant.frequency" required>
            <option value="One-time">One-time</option>
            <option value="Daily">Daily</option>
            <option value="Weekly">Weekly</option>
            <option value="Monthly">Monthly</option>
            <option value="Quarterly">Quarterly</option>
            <option value="Annually">Annually</option>
          </select>

          <label>Start Date:</label>
          <input type="date" v-model="editingGrant.start_date" required />
          
          <label>End Date:</label>
          <input type="date" v-model="editingGrant.end_date" />

          <div class="modal-actions">
            <button type="submit" class="save-button">Save</button>
            <button type="button" class="cancel-button" @click="cancelEdit">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Buttons Row -->
    <div class="buttons-row">
      <button class="add-button" @click="addGrant">Add Grant</button>
      <button class="export-button" @click="exportGrantsToExcel">Export Grants</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      grants: [],
      filters: {
        grant_name: '',
        start_date: '',
        end_date: '',
        frequency: '',
      },
      currentPage: 1,
      pageSize: 5,
      filteredGrants: [],
      editingGrant: null,
      showFilters: true
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredGrants.length / this.pageSize);
    },
    paginatedFilteredGrants() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredGrants.slice(start, end);
    },
  },
  methods: {
    async fetchGrants() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/grants/');
        this.grants = response.data;
        this.filteredGrants = this.grants;
      } catch (error) {
        console.error('Failed to fetch grants:', error);
      }
    },

    applyFilters() {
      this.filteredGrants = this.grants.filter(grant => {
        return (
          (this.filters.grant_name === '' || grant.grant_name.toLowerCase().includes(this.filters.grant_name.toLowerCase())) &&
          (this.filters.start_date === '' || grant.start_date === this.filters.start_date) &&
          (this.filters.end_date === '' || grant.end_date === this.filters.end_date) &&
          (this.filters.frequency === '' || grant.frequency === this.filters.frequency)
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

    async deleteGrant(id) {
      if (confirm('Are you sure you want to delete this grant?')) {
        try {
          await axios.delete(`http://127.0.0.1:5000/grants/${id}`);
          this.fetchGrants();
        } catch (error) {
          console.error('Failed to delete grant:', error);
        }
      }
    },

    editGrant(grant) {
      this.editingGrant = { ...grant };
    },

    async saveGrant() {
      try {
        if (this.editingGrant.id) {
          await axios.put(`http://127.0.0.1:5000/grants/${this.editingGrant.id}`, this.editingGrant);
        } else {
          await axios.post(`http://127.0.0.1:5000/grants/`, this.editingGrant);
        }
        this.editingGrant = null;
        this.fetchGrants();
      } catch (error) {
        console.error('Failed to save grant:', error);
      }
    },

    cancelEdit() {
      this.editingGrant = null;
    },

    addGrant() {
      this.editingGrant = { grant_name: '', purpose: '', amount: 0, frequency: 'One-time', start_date: '', end_date: '' };
    },

    async exportGrantsToExcel() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/grants/export');
        alert(response.data.message);
      } catch (error) {
        console.error('Failed to export grants:', error);
      }
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

    formatDate(date) {
      if (!date) return '';
      const [year, month, day] = date.split('-');
      return `${month}-${day}-${year}`;
    },
  },
  mounted() {
    this.fetchGrants();
  },
};
</script>

<style scoped>
.grants-page-container {
  max-width: 1200px;
  margin: 100px auto 20px auto;
  padding: 20px;
  background-color: #f7f9fa;
  border-radius: 8px;
  box-sizing: border-box;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.grants-page-container h1 {
  text-align:center;
  margin-bottom:30px;
  color:#2c3e50;
  font-size:28px;
}

/* Filters Panel */
.filters-panel {
  background-color:#fff;
  border-radius:8px;
  box-shadow:0 2px 4px rgba(0,0,0,0.1);
  padding:20px;
  margin-bottom:30px;
}

.filters-header {
  display:flex;
  justify-content:space-between;
  align-items:center;
}

.filters-header h2 {
  font-size:20px;
  color:#34495e;
  margin:0;
}

.toggle-button {
  background-color:#34495e;
  color:#ecf0f1;
  border:none;
  border-radius:4px;
  padding:6px 12px;
  cursor:pointer;
  font-weight:bold;
  transition:background-color 0.3s ease;
}

.toggle-button:hover {
  background-color:#2c3e50;
}

.fade-enter-active, .fade-leave-active {
  transition:opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity:0;
}

.filters-body {
  margin-top:20px;
}

.filters-grid {
  display:grid;
  grid-template-columns: repeat(auto-fill, minmax(180px,1fr));
  gap:20px;
}

.filter-item {
  display:flex;
  flex-direction:column;
}

.filter-item label {
  margin-bottom:5px;
  font-weight:bold;
  color:#34495e;
  font-size:14px;
}

.filter-item input, .filter-item select {
  padding:8px;
  border:1px solid #ccc;
  border-radius:4px;
  font-size:14px;
}

.filter-item input:focus, .filter-item select:focus {
  border-color:#42b983;
  outline:none;
}

.filters-actions {
  display:flex;
  justify-content:flex-end;
  gap:10px;
  margin-top:20px;
}

.apply-button, .reset-button {
  border:none;
  border-radius:4px;
  padding:8px 12px;
  cursor:pointer;
  font-weight:bold;
  color:#fff;
}

.apply-button {
  background-color:#42b983;
}
.apply-button:hover {
  background-color:#36a778;
}

.reset-button {
  background-color:#7f8c8d;
}
.reset-button:hover {
  background-color:#5f6f6f;
}

/* Table Container */
.table-container {
  overflow-x:auto;
  background-color:#fff;
  border-radius:8px;
  box-shadow:0 2px 4px rgba(0,0,0,0.1);
  padding:20px;
}

table {
  width:100%;
  border-collapse:collapse;
  background-color:#fff;
  overflow:hidden;
}

table th, table td {
  padding:12px;
  text-align:center;
  white-space:nowrap;
  font-size:14px;
}

table th {
  background-color:#34495e;
  color:#ecf0f1;
  font-weight:bold;
}

table tr:nth-child(even) {
  background-color:#f9f9f9;
}

table tr:hover {
  background-color:#f1f1f1;
}

.actions-cell {
  display:flex;
  justify-content:center;
  gap:5px;
}

.icon-button {
  border:none;
  background:none;
  cursor:pointer;
  font-size:16px;
}

.icon-button.edit:hover {
  color:#42b983;
}

.icon-button.delete:hover {
  color:#e74c3c;
}

/* Pagination */
.pagination {
  margin-top:20px;
  text-align:center;
  font-family:Arial, sans-serif;
  display:flex;
  justify-content:center;
  gap:20px;
  align-items:center;
}

.page-button {
  background-color:#34495e;
  color:#ecf0f1;
  border:none;
  border-radius:4px;
  padding:6px 12px;
  cursor:pointer;
  font-weight:bold;
  transition:background-color 0.3s ease;
}

.page-button:disabled {
  background-color:#7f8c8d;
  cursor:not-allowed;
}

.page-button:hover:enabled {
  background-color:#2c3e50;
}

/* Modal */
.modal-overlay {
  position:fixed;
  top:0; left:0; width:100%; height:100%;
  background-color:rgba(0,0,0,0.5);
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

.modal-form input, .modal-form textarea, .modal-form select {
  padding:8px;
  border:1px solid #ccc;
  border-radius:4px;
  font-size:14px;
}

.modal-form input:focus, .modal-form textarea:focus, .modal-form select:focus {
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

/* Buttons Row */
.buttons-row {
  margin-top:20px;
  display:flex;
  justify-content:space-between;
}

.add-button, .export-button {
  border:none;
  border-radius:4px;
  padding:8px 12px;
  cursor:pointer;
  font-weight:bold;
  color:#fff;
}

.add-button {
  background-color:#42b983;
}
.add-button:hover {
  background-color:#36a778;
}

.export-button {
  background-color:#3498db;
}
.export-button:hover {
  background-color:#2980b9;
}

/* Responsive */
@media (max-width:768px) {
  .filters-grid {
    grid-template-columns:1fr;
  }

  table th, table td {
    font-size:12px;
    padding:8px;
  }

  .page-button, .toggle-button, .apply-button, .reset-button, .add-button, .export-button {
    font-size:12px;
    padding:5px 10px;
  }

  .filter-item label {
    font-size:12px;
  }
}
</style>
