<template>
  <div class="events-page-container">
    <h1>Events Management</h1>

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
              <label>Event Name</label>
              <input type="text" v-model="filters.event_name" placeholder="Search by name" />
            </div>
            <div class="filter-item">
              <label>Event Date</label>
              <input type="date" v-model="filters.event_date" />
            </div>
            <div class="filter-item">
              <label>Location</label>
              <input type="text" v-model="filters.location" placeholder="Search by location" />
            </div>
            <div class="filter-item">
              <label>Event Type</label>
              <input type="text" v-model="filters.event_type" placeholder="Search by type" />
            </div>
          </div>
          <div class="filters-actions">
            <button class="apply-button" @click="applyFilters">Apply</button>
            <button class="reset-button" @click="resetFilters">Reset</button>
          </div>
        </div>
      </transition>
    </div>

    <!-- Events Table -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Event Name</th>
            <th>Event Date</th>
            <th>Location</th>
            <th>Event Type</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="event in paginatedFilteredEvents" :key="event.id">
            <td>{{ event.event_name }}</td>
            <td>{{ formatDisplayDate(event.event_date) }}</td>
            <td>{{ event.location }}</td>
            <td>{{ event.event_type }}</td>
            <td class="actions-cell">
              <button class="icon-button edit" @click="editEvent(event)" title="Edit">✏️</button>
              <button class="icon-button delete" @click="deleteEvent(event.id)" title="Delete">🗑️</button>
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

    <!-- Edit Event Modal -->
    <div v-if="editingEvent" class="modal-overlay" @click.self="cancelEdit">
      <div class="modal-content">
        <h2>Edit Event</h2>
        <form @submit.prevent="saveEvent" class="modal-form">
          <label>Event Name:</label>
          <input type="text" v-model="editingEvent.event_name" required />
          
          <label>Event Date:</label>
          <input type="date" v-model="editingEvent.event_date" required />
          
          <label>Location:</label>
          <input type="text" v-model="editingEvent.location" required />
          
          <label>Event Type:</label>
          <input type="text" v-model="editingEvent.event_type" required />
          
          <label>Content:</label>
          <textarea v-model="editingEvent.content" required></textarea>

          <div class="modal-actions">
            <button type="submit" class="save-button">Save</button>
            <button type="button" class="cancel-button" @click="cancelEdit">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Export Button -->
    <button class="export-button" @click="exportEventsToExcel">Export Events</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      events: [],
      filters: {
        event_name: '',
        event_date: '',
        location: '',
        event_type: '',
      },
      currentPage: 1,
      pageSize: 5,
      filteredEvents: [],
      editingEvent: null,
      showFilters: true
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredEvents.length / this.pageSize);
    },
    paginatedFilteredEvents() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredEvents.slice(start, end);
    },
  },
  methods: {
    async fetchEvents() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/events/');
        this.events = response.data;
        this.filteredEvents = this.events;
      } catch (error) {
        console.error('Failed to fetch events:', error);
      }
    },

    applyFilters() {
      this.filteredEvents = this.events.filter(event => {
        return (
          (this.filters.event_name === '' || event.event_name.toLowerCase().includes(this.filters.event_name.toLowerCase())) &&
          (this.filters.event_date === '' || event.event_date === this.filters.event_date) &&
          (this.filters.location === '' || event.location.toLowerCase().includes(this.filters.location.toLowerCase())) &&
          (this.filters.event_type === '' || event.event_type.toLowerCase().includes(this.filters.event_type.toLowerCase()))
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

    async deleteEvent(id) {
      if (confirm('Are you sure you want to delete this event?')) {
        try {
          await axios.delete(`http://127.0.0.1:5000/events/${id}`);
          this.fetchEvents();
        } catch (error) {
          console.error('Failed to delete event:', error);
        }
      }
    },

    editEvent(event) {
      this.editingEvent = { ...event };
    },

    async saveEvent() {
      try {
        await axios.put(`http://127.0.0.1:5000/events/${this.editingEvent.id}`, this.editingEvent);
        this.editingEvent = null;
        this.fetchEvents();
      } catch (error) {
        console.error('Failed to save event:', error);
      }
    },

    cancelEdit() {
      this.editingEvent = null;
    },

    async exportEventsToExcel() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/events/export');
        alert(response.data.message);
      } catch (error) {
        console.error('Failed to export events:', error);
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

    // 将 YYYY-MM-DD 转换为 MM-DD-YYYY 显示
    formatDisplayDate(date) {
      if (!date) return '';
      const [year, month, day] = date.split('-');
      return `${month}-${day}-${year}`;
    },
  },
  mounted() {
    this.fetchEvents();
  },
};
</script>

<style scoped>
.events-page-container {
  max-width: 1200px;
  margin: 100px auto 20px auto;
  padding: 20px;
  background-color: #f7f9fa;
  border-radius: 8px;
  box-sizing: border-box;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.events-page-container h1 {
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
  grid-template-columns: repeat(auto-fill, minmax(180px,1fr));
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

.filter-item input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius:4px;
  font-size:14px;
}

.filter-item input:focus {
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

.modal-form input, .modal-form textarea {
  padding:8px;
  border:1px solid #ccc;
  border-radius:4px;
  font-size:14px;
}

.modal-form input:focus, .modal-form textarea:focus {
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

/* Export Button */
.export-button {
  margin-top:20px;
  background-color:#3498db;
  color:#fff;
  border:none;
  border-radius:4px;
  padding:8px 12px;
  cursor:pointer;
  font-weight:bold;
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

  .page-button, .toggle-button, .apply-button, .reset-button, .export-button {
    font-size:12px;
    padding:5px 10px;
  }

  .filter-item label {
    font-size:12px;
  }
}
</style>
