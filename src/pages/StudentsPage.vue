<template>
  <div class="students-page-container">
    <h1>Students Management</h1>

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
              <label>Course</label>
              <input type="text" v-model="filters.course" />
            </div>
            <div class="filter-item">
              <label>City</label>
              <input type="text" v-model="filters.city" />
            </div>
            <div class="filter-item">
              <label>Country</label>
              <input type="text" v-model="filters.country" />
            </div>
            <div class="filter-item">
              <label>Student Type</label>
              <select v-model="filters.student_type">
                <option value="">All</option>
                <option value="current">Current</option>
                <option value="alumni">Alumni</option>
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
            <th>Course</th>
            <th>City</th>
            <th>Country</th>
            <th>Student Type</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="student in paginatedFilteredStudents" :key="student.id">
            <td>{{ student.id }}</td>
            <td>{{ student.first_name }}</td>
            <td>{{ student.last_name }}</td>
            <td>{{ student.email }}</td>
            <td>{{ student.phone }}</td>
            <td>{{ student.course }}</td>
            <td>{{ student.city }}</td>
            <td>{{ student.country }}</td>
            <td>{{ student.student_type }}</td>
            <td class="actions-cell">
              <button class="icon-button edit" @click="editStudent(student)" title="Edit">
                ✏️
              </button>
              <button class="icon-button delete" @click="deleteStudent(student.id)" title="Delete">
                🗑️
              </button>
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

    <!-- Edit Student Modal -->
    <div v-if="editingStudent" class="modal-overlay" @click.self="cancelEdit">
      <div class="modal-content">
        <h2>Edit Student</h2>
        <form @submit.prevent="saveStudent" class="modal-form">
          <label>First Name:</label>
          <input type="text" v-model="editingStudent.first_name" required />
          <label>Last Name:</label>
          <input type="text" v-model="editingStudent.last_name" required />
          <label>Email:</label>
          <input type="email" v-model="editingStudent.email" required />
          <label>Phone:</label>
          <input type="text" v-model="editingStudent.phone" required />
          <label>Course:</label>
          <input type="text" v-model="editingStudent.course" required />
          <label>City:</label>
          <input type="text" v-model="editingStudent.city" required />
          <label>Country:</label>
          <input type="text" v-model="editingStudent.country" required />
          <label>Student Type:</label>
          <input type="text" v-model="editingStudent.student_type" required />

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
      students: [],
      filters: {
        id: '',
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        course: '',
        city: '',
        country: '',
        student_type: '',
      },
      currentPage: 1,
      pageSize: 5,
      filteredStudents: [],
      editingStudent: null,
      showFilters: true
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredStudents.length / this.pageSize);
    },
    paginatedFilteredStudents() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredStudents.slice(start, end);
    },
  },
  methods: {
    async fetchStudents() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/students/');
        this.students = response.data;
        this.filteredStudents = this.students;
      } catch (error) {
        console.error('Failed to fetch students:', error);
      }
    },
    applyFilters() {
      this.filteredStudents = this.students.filter(student => {
        return (
          (this.filters.id === '' || student.id === Number(this.filters.id)) &&
          (this.filters.first_name === '' || student.first_name.toLowerCase().includes(this.filters.first_name.toLowerCase())) &&
          (this.filters.last_name === '' || student.last_name.toLowerCase().includes(this.filters.last_name.toLowerCase())) &&
          (this.filters.email === '' || student.email.toLowerCase().includes(this.filters.email.toLowerCase())) &&
          (this.filters.phone === '' || student.phone.toLowerCase().includes(this.filters.phone.toLowerCase())) &&
          (this.filters.course === '' || student.course.toLowerCase().includes(this.filters.course.toLowerCase())) &&
          (this.filters.city === '' || student.city.toLowerCase().includes(this.filters.city.toLowerCase())) &&
          (this.filters.country === '' || student.country.toLowerCase().includes(this.filters.country.toLowerCase())) &&
          (this.filters.student_type === '' || 
 student.student_type.toLowerCase() === this.filters.student_type.toLowerCase())

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
    async deleteStudent(id) {
      if (confirm('Are you sure you want to delete this student?')) {
        try {
          await axios.delete(`http://127.0.0.1:5000/students/${id}`);
          this.fetchStudents();
        } catch (error) {
          console.error('Failed to delete student:', error);
        }
      }
    },
    editStudent(student) {
      this.editingStudent = { ...student };
    },
    async saveStudent() {
      try {
        await axios.put(`http://127.0.0.1:5000/students/${this.editingStudent.id}`, this.editingStudent);
        this.editingStudent = null;
        this.fetchStudents();
      } catch (error) {
        console.error('Failed to save student:', error);
      }
    },
    cancelEdit() {
      this.editingStudent = null;
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
    this.fetchStudents();
  },
};
</script>

<style scoped>
.students-page-container {
  max-width: 1200px;
  margin: 100px auto 20px auto;
  padding: 20px;
  background-color: #f7f9fa;
  border-radius: 8px;
  box-sizing: border-box;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.students-page-container h1 {
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

.filter-item input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius:4px;
  font-size: 14px;
}

.filter-item input:focus {
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

.modal-form input {
  padding:8px;
  border:1px solid #ccc;
  border-radius:4px;
}

.modal-form input:focus {
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
