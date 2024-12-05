<template>
  <div class="interactions-page">
    <h1>Interactions Management</h1>
    <!-- 搜索栏 -->
    <div class="search-bar">
      <input type="text" v-model="searchQuery" placeholder="Search by student or contact" />
    </div>

    <!-- 按钮：添加新交互 -->
    <button class="add-button" @click="showAddModal = true">Add Interaction</button>

    <!-- 统计结果展示 -->
    <h2>Summary</h2>
    <div class="summary-section">
      <h3>Student Participation</h3>
      <table>
        <thead>
          <tr>
            <th>Student Name</th>
            <th>Events Participated</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in studentEventsSummary" :key="item.name" @click="viewPersonDetails(item.name, 'student')">
            <td>{{ item.name }}</td>
            <td>{{ item.eventsParticipated }}</td>
          </tr>
        </tbody>
      </table>

      <h3>Contact Participation</h3>
      <table>
        <thead>
          <tr>
            <th>Contact Name</th>
            <th>Events Participated</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in contactEventsSummary" :key="item.name" @click="viewPersonDetails(item.name, 'contact')">
            <td>{{ item.name }}</td>
            <td>{{ item.eventsParticipated }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Interactions 列表展示（可分页） -->
    <h2>All Interactions</h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Student Name</th>
          <th>Contact Name</th>
          <th>Event Name</th>
          <th>Interaction Type</th>
          <th>Notes</th>
          <th>Created At</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="interaction in paginatedFilteredInteractions" :key="interaction.id">
          <td>{{ interaction.id }}</td>
          <td>{{ interaction.student_name }}</td>
          <td>{{ interaction.contact_name }}</td>
          <td>{{ interaction.event_name }}</td>
          <td>{{ interaction.interaction_type }}</td>
          <td>{{ interaction.notes }}</td>
          <td>{{ interaction.created_at }}</td>
        </tr>
      </tbody>
    </table>

    <!-- 分页控件 -->
    <div class="pagination">
      <button :disabled="currentPage === 1" @click="prevPage">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="nextPage">Next</button>
    </div>

    <!-- 添加 Interaction 的弹窗 -->
    <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
      <div class="modal-content">
        <h2>Add Interaction</h2>
        <form @submit.prevent="addInteraction">
          <label>Student ID (optional):</label>
          <input type="number" v-model="newInteraction.student_id" />
          <label>Contact ID (optional):</label>
          <input type="number" v-model="newInteraction.contact_id" />
          <label>Event ID (required):</label>
          <input type="number" v-model="newInteraction.event_id" required />
          <label>Interaction Type ID (optional):</label>
          <input type="number" v-model="newInteraction.interaction_type_id" />
          <label>Notes:</label>
          <textarea v-model="newInteraction.notes"></textarea>
          <div class="modal-actions">
            <button type="submit">Save</button>
            <button type="button" @click="showAddModal = false">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 侧边栏：显示特定学生或联系人的参与事件详情 -->
    <div v-if="personDetailVisible" class="sidebar">
      <h2>{{ currentPersonType === 'student' ? 'Student' : 'Contact' }}: {{ currentPersonName }}</h2>
      <h3>Events Participated</h3>
      <ul>
        <li v-for="evt in personEvents" :key="evt">{{ evt }}</li>
      </ul>
      <button @click="personDetailVisible = false">Close</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      interactions: [],
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      showAddModal: false,
      newInteraction: {
        student_id: null,
        contact_id: null,
        event_id: null,
        interaction_type_id: null,
        notes: ''
      },
      personDetailVisible: false,
      currentPersonName: '',
      currentPersonType: '', // 'student' or 'contact'
      personEvents: []
    };
  },
  computed: {
    filteredInteractions() {
      if (!this.searchQuery.trim()) {
        return this.interactions;
      }
      const query = this.searchQuery.toLowerCase();
      return this.interactions.filter(interaction => {
        const studentName = interaction.student_name ? interaction.student_name.toLowerCase() : '';
        const contactName = interaction.contact_name ? interaction.contact_name.toLowerCase() : '';
        return studentName.includes(query) || contactName.includes(query);
      });
    },
    paginatedFilteredInteractions() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredInteractions.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredInteractions.length / this.pageSize);
    },
    studentEventsSummary() {
      const studentEventsCount = {};
      this.interactions.forEach(interaction => {
        const { student_name, event_name } = interaction;
        if (student_name) {
          if (!studentEventsCount[student_name]) {
            studentEventsCount[student_name] = new Set();
          }
          studentEventsCount[student_name].add(event_name);
        }
      });
      return Object.entries(studentEventsCount).map(([name, eventsSet]) => ({
        name,
        eventsParticipated: eventsSet.size
      }));
    },
    contactEventsSummary() {
      const contactEventsCount = {};
      this.interactions.forEach(interaction => {
        const { contact_name, event_name } = interaction;
        if (contact_name) {
          if (!contactEventsCount[contact_name]) {
            contactEventsCount[contact_name] = new Set();
          }
          contactEventsCount[contact_name].add(event_name);
        }
      });
      return Object.entries(contactEventsCount).map(([name, eventsSet]) => ({
        name,
        eventsParticipated: eventsSet.size
      }));
    }
  },
  methods: {
    fetchInteractions() {
      axios.get('/interactions/')
        .then(response => {
          this.interactions = response.data;
        })
        .catch(error => {
          console.error('Error fetching interactions:', error);
        });
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
    addInteraction() {
      axios.post('/interactions/', this.newInteraction)
        .then(() => {
          this.showAddModal = false;
          // 重置表单
          this.newInteraction = {
            student_id: null,
            contact_id: null,
            event_id: null,
            interaction_type_id: null,
            notes: ''
          };
          // 刷新列表
          this.fetchInteractions();
        })
        .catch(error => {
          console.error('Error adding interaction:', error);
        });
    },
    viewPersonDetails(name, type) {
      // 根据 name 和 type (student or contact) 在前端筛选出此人参与的所有事件
      let eventsSet = new Set();
      this.interactions.forEach(interaction => {
        if (type === 'student' && interaction.student_name === name) {
          eventsSet.add(interaction.event_name);
        }
        if (type === 'contact' && interaction.contact_name === name) {
          eventsSet.add(interaction.event_name);
        }
      });
      this.personEvents = Array.from(eventsSet);
      this.currentPersonName = name;
      this.currentPersonType = type;
      this.personDetailVisible = true;
    }
  },
  mounted() {
    this.fetchInteractions();
  }
};
</script>

<style scoped>
.interactions-page {
  max-width: 1200px;
  margin: 80px auto;
  background-color: #f7f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  font-family: Arial, sans-serif;
}

.search-bar {
  margin-bottom: 20px;
}

.search-bar input {
  padding: 6px 10px;
  border: 1px solid #ccc;
  border-radius:4px;
}

.add-button {
  background-color:#42b983;
  color:#fff;
  border:none;
  border-radius:4px;
  padding:8px 12px;
  cursor:pointer;
  font-weight:bold;
  margin-bottom:20px;
}

.add-button:hover {
  background-color:#36a778;
}

.summary-section {
  margin-bottom:40px;
}

summary-section table {
  margin-bottom:20px;
}

table {
  width:100%;
  border-collapse: collapse;
  margin-top:20px;
  background-color:#fff;
  border-radius:8px;
  overflow:hidden;
}

table th, table td {
  padding:12px;
  text-align:center;
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
  cursor:pointer;
}

.pagination {
  margin-top:20px;
  text-align:center;
  display:flex;
  justify-content:center;
  gap:20px;
  align-items:center;
}

.pagination button {
  background-color:#34495e;
  color:#ecf0f1;
  border:none;
  border-radius:4px;
  padding:6px 12px;
  cursor:pointer;
  font-weight:bold;
}

.pagination button:disabled {
  background-color:#7f8c8d;
  cursor:not-allowed;
}

.pagination button:hover:enabled {
  background-color:#2c3e50;
}

.modal-overlay {
  position:fixed;
  top:0; left:0; width:100%; height:100%;
  background-color:rgba(0,0,0,0.5);
  display:flex;
  justify-content:center;
  align-items:center;
  z-index:2000;
}

.modal-content {
  background-color:#fff;
  padding:30px;
  border-radius:8px;
  max-width:400px;
  width:100%;
  box-sizing:border-box;
}

.modal-content h2 {
  text-align:center;
  margin-bottom:20px;
  color:#2c3e50;
}

.modal-content form {
  display:flex;
  flex-direction:column;
  gap:10px;
}

.modal-content form label {
  font-weight:bold;
  margin-bottom:4px;
  color:#34495e;
}

.modal-content form input, .modal-content form textarea {
  padding:8px;
  border:1px solid #ccc;
  border-radius:4px;
  font-size:14px;
}

.modal-content form textarea {
  resize:vertical;
}

.modal-actions {
  display:flex;
  justify-content:flex-end;
  gap:10px;
  margin-top:20px;
}

.modal-actions button {
  border:none;
  border-radius:4px;
  padding:8px 12px;
  cursor:pointer;
  font-weight:bold;
  color:#fff;
}

.modal-actions button[type="submit"] {
  background-color:#42b983;
}
.modal-actions button[type="submit"]:hover {
  background-color:#36a778;
}

.modal-actions button[type="button"] {
  background-color:#7f8c8d;
}
.modal-actions button[type="button"]:hover {
  background-color:#5f6f6f;
}

.sidebar {
  position:fixed;
  top:0;
  right:0;
  width:300px;
  height:100%;
  background-color:#fff;
  box-shadow:-2px 0 6px rgba(0,0,0,0.1);
  padding:20px;
  overflow:auto;
  z-index:2100;
}

.sidebar h2 {
  margin-top:0;
  color:#2c3e50;
}

.sidebar h3 {
  margin-bottom:10px;
}

.sidebar button {
  background-color:#7f8c8d;
  color:#fff;
  border:none;
  border-radius:4px;
  padding:8px 12px;
  cursor:pointer;
  font-weight:bold;
  margin-top:20px;
}

.sidebar button:hover {
  background-color:#5f6f6f;
}
</style>
