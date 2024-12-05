<template>
  <div>
    <!-- Fixed navbar at the top -->
    <nav class="navbar">
      <div class="navbar-container">
        <ul class="navbar-links">
          <li><router-link to="/dashboard" class="custom-link">Dashboard</router-link></li>
          <li><router-link to="/students" class="custom-link">Students</router-link></li>
          <li><router-link to="/contacts" class="custom-link">Contacts</router-link></li>
          <li><router-link to="/events" class="custom-link">Events</router-link></li>
          <li><router-link to="/grants" class="custom-link">Grants</router-link></li>
          <li><router-link to="/interactions" class="custom-link">Interactions</router-link></li>
          <li><router-link to="/add-data" class="custom-link">Add Data</router-link></li>
          <li><router-link to="/register" class="custom-link">Register User</router-link></li>
          <li><button @click="logout" class="logout-button">Logout</button></li>
        </ul>
      </div>
    </nav>
    <!-- Page container to prevent content from touching the screen edges and to center it -->
    <div class="page-container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    // Logout method: remove the token and redirect to the login page
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
/* Navbar styles */
.navbar {
  background-color: #2c3e50;
  position: fixed;
  width: 100%;
  top: 0;
  left: 0;
  z-index: 100;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Navbar container to center navigation links */
.navbar-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Navigation links list */
.navbar-links {
  list-style: none;
  display: flex;
  gap: 30px;
  margin: 0;
  padding: 0;
}

/* Common link styles */
.custom-link {
  color: #42b983;
  font-family: 'Arial', sans-serif;
  font-size: 16px;
  text-decoration: none;
  transition: color 0.3s ease, border-bottom 0.3s ease;
}

/* Hover effect for links */
.custom-link:hover {
  color: #ff6347;
  border-bottom: 2px solid #ff6347;
}

/* Logout button styled like links */
.logout-button {
  background: none;
  border: none;
  color: #42b983;
  font-family: 'Arial', sans-serif;
  font-size: 16px;
  cursor: pointer;
  transition: color 0.3s ease, border-bottom 0.3s ease;
}

.logout-button:hover {
  color: #ff6347;
  border-bottom: 2px solid #ff6347;
}

/* Page container to control maximum width and padding */
.page-container {
  max-width: 1200px; 
  margin: 100px auto 20px auto; /* Leave space for the navbar, center content horizontally */
  padding: 20px; /* Add padding so content won't touch the screen edges */
  box-sizing: border-box;
}

/* Base body styles */
body {
  font-family: Arial, sans-serif;
  color: #333;
  margin: 0;
}

/* Headings */
h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
}

h3 {
  margin-bottom: 15px;
  color: #34495e;
}

/* Example overview section (adjust as needed) */
.overview {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  gap: 20px;
  margin-bottom: 30px;
}

.overview-item {
  flex: 1 1 calc(25% - 20px);
  text-align: center;
  padding: 20px;
  background-color: #ecf0f1;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.overview-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.2);
}

/* Charts section (adjust as needed) */
.charts {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 20px;
}

.chart {
  flex: 1 1 calc(50% - 20px);
  padding: 15px;
  background-color: #ecf0f1;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Tables section (adjust as needed) */
.tables {
  margin-top: 30px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

table th, table td {
  padding: 12px;
  text-align: center;
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

/* Responsive design: single-column layout on smaller screens */
@media (max-width: 768px) {
  .overview,
  .charts {
    flex-direction: column;
  }

  .overview-item,
  .chart {
    flex: 1 1 100%;
  }

  table th, table td {
    font-size: 14px;
    padding: 8px;
  }

  .navbar-links {
    gap: 15px;
  }
}
</style>
