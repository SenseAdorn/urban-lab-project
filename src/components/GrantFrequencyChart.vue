<template>
    <div>
      <h3>Grant Frequency Distribution</h3>
      <canvas id="grantFrequencyChart" width="400" height="400"></canvas>
    </div>
  </template>
  
  <script>
  import { Pie } from 'vue-chartjs';
  import { Chart as ChartJS } from 'chart.js';
  import { reactive, onMounted } from 'vue';
  
  export default {
    name: 'GrantFrequencyChart',
    components: {
      Pie,
    },
    setup() {
      const chartData = reactive({
        labels: ['One-time', 'Daily', 'Weekly', 'Monthly', 'Quarterly', 'Annually'],
        datasets: [{
          data: [0, 0, 0, 0, 0, 0], // 默认值
          backgroundColor: ['#FF5733', '#33FF57', '#3357FF', '#FF33A6', '#FF8C00', '#8B33FF'],
        }],
      });
  
      // 从后端 API 获取数据
      onMounted(() => {
        fetch('/api/grant_frequency_distribution')
          .then(response => response.json())
          .then(data => {
            // 更新数据
            data.forEach(item => {
              const index = chartData.labels.indexOf(item.frequency);
              if (index !== -1) {
                chartData.datasets[0].data[index] = item.count;
              }
            });
          })
          .catch(error => console.error('Error fetching data:', error));
      });
  
      return { chartData };
    },
  };
  </script>
  
  <style scoped>
  /* 可根据需求修改样式 */
  #grantFrequencyChart {
    max-width: 600px;
    margin: 0 auto;
  }
  </style>
  