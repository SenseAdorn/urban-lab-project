<template>
  <div class="page-container">
    <!-- 顶部导航条 -->
    <header class="top-nav">
      <div class="brand">My Dashboard</div>
      <nav>
        <a href="#" @click.prevent>Home</a>
        <a href="#" @click.prevent>Reports</a>
        <a href="#" @click.prevent>Settings</a>
      </nav>
    </header>

    <div class="dashboard-content">
      <!-- Overview Section -->
      <section class="overview-section">
        <h2 class="section-title">Overview</h2>
        <div class="overview">
          <div class="overview-item">
            <div class="icon-container">
              <i class="fas fa-address-book"></i>
            </div>
            <h3>Total Contacts</h3>
            <p>{{ totalContacts }}</p>
          </div>
          <div class="overview-item">
            <div class="icon-container">
              <i class="fas fa-user-graduate"></i>
            </div>
            <h3>Total Students</h3>
            <p>{{ totalStudents }}</p>
          </div>
          <div class="overview-item">
            <div class="icon-container">
              <i class="fas fa-hand-holding-usd"></i>
            </div>
            <h3>Total Grants</h3>
            <p>{{ totalGrants }}</p>
          </div>
          <div class="overview-item">
            <div class="icon-container">
              <i class="fas fa-calendar-alt"></i>
            </div>
            <h3>Total Events</h3>
            <p>{{ totalEvents }}</p>
          </div>
        </div>
      </section>

      <!-- Chart Section -->
      <section class="charts-section">
        <h2 class="section-title">Analytics</h2>
        <div class="charts">
          <div class="chart-card">
            <h3>Grant Frequency Distribution</h3>
            <PieChart :data="grantFrequencyData" :options="{ maintainAspectRatio: false }" />
          </div>
          <div class="chart-card">
            <h3>Event Trend</h3>
            <LineChart :data="studentAgeLineData" :options="{ maintainAspectRatio: false }" />
          </div>
        </div>
      </section>

      <!-- Data Tables Section -->
      <section class="tables-section">
        <h2 class="section-title">Recent Records</h2>

        <div class="table-card">
          <h3>Recent Contacts</h3>
          <table>
            <thead>
              <tr>
                <th>Name</th><th>Email</th><th>Phone</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="contact in recentContacts" :key="contact.id">
                <td>{{ contact.first_name }} {{ contact.last_name }}</td>
                <td>{{ contact.email }}</td>
                <td>{{ contact.phone }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="table-card">
          <h3>Recent Students</h3>
          <table>
            <thead>
              <tr>
                <th>Student Name</th><th>Email</th><th>Course</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in recentStudents" :key="student.id">
                <td>{{ student.first_name }} {{ student.last_name }}</td>
                <td>{{ student.email }}</td>
                <td>{{ student.course }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="table-card">
          <h3>Recent Events</h3>
          <table>
            <thead>
              <tr>
                <th>Event Name</th><th>Location</th><th>Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="event in recentEvents" :key="event.id">
                <td>{{ event.event_name }}</td>
                <td>{{ event.location }}</td>
                <td>{{ formatDate(event.event_date) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="table-card">
          <h3>Recent Grants</h3>
          <table>
            <thead>
              <tr>
                <th>Grant Name</th><th>Amount</th><th>Frequency</th><th>Start Date</th><th>End Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="grant in recentGrants" :key="grant.id">
                <td>{{ grant.grant_name }}</td>
                <td>{{ grant.amount }}</td>
                <td>{{ grant.frequency }}</td>
                <td>{{ formatDate(grant.start_date) }}</td>
                <td>{{ grant.end_date ? formatDate(grant.end_date) : 'N/A' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Pie, Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale, PointElement, LineElement);

export default {
  components: {
    PieChart: Pie,
    LineChart: Line
  },
  data() {
    return {
      totalContacts: 0,
      totalStudents: 0,
      totalEvents: 0,
      totalGrants: 0,
      grantFrequencyData: {
        labels: ['One-time', 'Daily', 'Weekly', 'Monthly', 'Quarterly', 'Annually'],
        datasets: [
          {
            data: [20, 5, 10, 15, 5, 45],
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
          },
        ],
      },
      // 将原先的 studentAgeData 转为线图数据
      studentAgeLineData: {
        labels: ['2021', '2022', '2023', '2024', '2025'],
        datasets: [
          {
            label: 'Event Trend',
            data: [10, 25, 35, 15, 5],
            fill: false,
            borderColor: '#42A5F5',
            tension: 0.3,
            pointBackgroundColor: '#fff',
            pointBorderColor: '#42A5F5',
            pointRadius: 5
          },
        ],
      },
      recentContacts: [],
      recentStudents: [],
      recentEvents: [],
      recentGrants: [],
    };
  },
  methods: {
    async fetchData() {
      try {
        const [contactsResponse, studentsResponse, eventsResponse, grantsResponse] = await Promise.all([
          axios.get('http://127.0.0.1:5000/contacts/'),
          axios.get('http://127.0.0.1:5000/students/'),
          axios.get('http://127.0.0.1:5000/events/'),
          axios.get('http://127.0.0.1:5000/grants/')
        ]);

        this.recentContacts = contactsResponse.data.slice(0, 5);
        this.recentStudents = studentsResponse.data.slice(0, 5);
        this.recentEvents = eventsResponse.data.slice(0, 5);
        this.recentGrants = grantsResponse.data.slice(0, 5);

        this.totalContacts = contactsResponse.data.length;
        this.totalStudents = studentsResponse.data.length;
        this.totalEvents = eventsResponse.data.length;
        this.totalGrants = grantsResponse.data.length;

      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    },
    formatDate(date) {
      const [year, month, day] = date.split('-');
      return `${month}-${day}-${year}`;
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style scoped>
body {
  margin:0;
  background:#f0f2f5;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 顶部导航条 */
.top-nav {
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:20px;
  background:#34495e;
  color:#ecf0f1;
}

.top-nav .brand {
  font-size:20px;
  font-weight:bold;
}

.top-nav nav a {
  color:#ecf0f1;
  text-decoration:none;
  margin-left:20px;
  font-size:14px;
}
.top-nav nav a:hover {
  text-decoration:underline;
}

/* 页面容器 */
.page-container {
  display:flex;
  flex-direction:column;
}

/* Dashboard 内容区域 */
.dashboard-content {
  max-width:1200px;
  margin:40px auto;
  padding:20px;
  background:#fff;
  border-radius:8px;
  box-shadow:0 2px 6px rgba(0,0,0,0.1);
}

/* 标题 */
.section-title {
  font-size:24px;
  color:#2c3e50;
  margin-bottom:30px;
  text-align:left;
  font-weight:bold;
}

/* Overview Section */
.overview-section {
  margin-bottom:40px;
}

.overview {
  display:flex;
  flex-wrap:wrap;
  gap:20px;
  justify-content:space-between;
}

.overview-item {
  flex:1 1 calc(25% - 20px);
  background: linear-gradient(135deg, #42b983, #36a778);
  color:#fff;
  padding:20px;
  border-radius:8px;
  text-align:center;
  transition:transform 0.3s ease, box-shadow 0.3s ease;
  position:relative;
}

.overview-item h3 {
  margin:10px 0;
  font-size:16px;
  font-weight:bold;
}

.overview-item p {
  font-size:24px;
  font-weight:bold;
  margin:0;
}

.overview-item:hover {
  transform:translateY(-5px);
  box-shadow:0 6px 12px rgba(0,0,0,0.2);
}

.icon-container {
  font-size:30px;
  margin-bottom:10px;
}

/* Charts Section */
.charts-section {
  margin-bottom:40px;
}

.charts {
  display:flex;
  flex-wrap:wrap;
  gap:20px;
  justify-content:center;
}

.chart-card {
  background:#ecf0f1;
  border-radius:8px;
  box-shadow:0 4px 6px rgba(0,0,0,0.1);
  padding:20px;
  width:300px;
  height:320px;
  display:flex;
  flex-direction:column;
  justify-content:flex-start;
  align-items:center;
}

.chart-card h3 {
  margin-bottom:10px;
  font-size:16px;
  text-align:center;
  color:#34495e;
}

/* Tables Section */
.tables-section {
  margin-bottom:40px;
}

.table-card {
  background:#fff;
  border-radius:8px;
  box-shadow:0 4px 6px rgba(0,0,0,0.1);
  padding:20px;
  margin-bottom:30px;
}

.table-card h3 {
  margin-bottom:20px;
  color:#34495e;
  font-size:18px;
  font-weight:bold;
}

table {
  width:100%;
  border-collapse:collapse;
  background:#fff;
  border-radius:8px;
  overflow:hidden;
}

table th, table td {
  padding:12px;
  text-align:center;
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

@media (max-width:768px) {
  .overview {
    flex-direction:column;
    gap:20px;
  }

  .charts {
    flex-direction:column;
  }

  .chart-card {
    width:100%;
    max-width:400px;
    margin:0 auto;
  }
}
</style>
