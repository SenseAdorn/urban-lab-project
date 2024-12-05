<template>
  <div class="add-data-container">
    <h1>Add New Data</h1>
    
    <div class="module-selector">
      <label for="data-type">Choose a module:</label>
      <select id="data-type" v-model="selectedModule" @change="loadFields">
        <option value="" disabled>Select a module</option>
        <option value="contacts">Contacts</option>
        <option value="students">Students</option>
        <option value="events">Events</option>
        <option value="grants">Grants</option>
      </select>
    </div>

    <form v-if="selectedModule" @submit.prevent="submitData" class="data-form">
      <div v-for="field in fields" :key="field.name" class="form-group">
        <label :for="field.name" class="form-label">{{ field.label }}:</label>
        <div class="form-input-wrapper">
          <input
            v-if="field.type !== 'textarea'"
            :type="field.type"
            :id="field.name"
            v-model="formData[field.name]"
            :placeholder="field.placeholder"
            :required="field.required"
            class="form-input"
          />
          <textarea
            v-else
            :id="field.name"
            v-model="formData[field.name]"
            :placeholder="field.placeholder"
            :required="field.required"
            class="form-textarea"
          ></textarea>
        </div>
      </div>
      <button type="submit" class="submit-button">Submit</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedModule: "", // Currently selected module
      fields: [], // Form fields dynamically generated
      formData: {}, // Form data to be submitted
    };
  },
  methods: {
    // Load form fields dynamically based on the selected module
    loadFields() {
      const modulesConfig = {
        contacts: [
          { name: "first_name", label: "First Name", type: "text", placeholder: "Enter first name", required: true },
          { name: "last_name", label: "Last Name", type: "text", placeholder: "Enter last name", required: true },
          { name: "email", label: "Email", type: "email", placeholder: "Enter email", required: true },
          { name: "phone", label: "Phone", type: "text", placeholder: "Enter phone number", required: false },
          { name: "role_id", label: "Role ID", type: "number", placeholder: "Enter role ID", required: false },
          { name: "organization", label: "Organization", type: "text", placeholder: "Enter organization", required: false },
          { name: "city", label: "City", type: "text", placeholder: "Enter city", required: false },
          { name: "country", label: "Country", type: "text", placeholder: "Enter country", required: false },
          { name: "notes", label: "Notes", type: "textarea", placeholder: "Enter additional notes", required: false },
        ],
        students: [
          { name: "first_name", label: "First Name", type: "text", placeholder: "Enter first name", required: true },
          { name: "last_name", label: "Last Name", type: "text", placeholder: "Enter last name", required: true },
          { name: "email", label: "Email", type: "email", placeholder: "Enter email", required: true },
          { name: "phone", label: "Phone", type: "text", placeholder: "Enter phone number", required: false },
          { name: "course", label: "Course", type: "text", placeholder: "Enter course", required: false },
          { name: "city", label: "City", type: "text", placeholder: "Enter city", required: false },
          { name: "country", label: "Country", type: "text", placeholder: "Enter country", required: false },
          { name: "student_type", label: "Student Type", type: "text", placeholder: "Enter student type", required: false },
        ],
        events: [
          { name: "event_name", label: "Event Name", type: "text", placeholder: "Enter event name", required: true },
          { name: "event_date", label: "Event Date", type: "date", placeholder: "Enter event date", required: true },
          { name: "location", label: "Location", type: "text", placeholder: "Enter location", required: false },
          { name: "event_type", label: "Event Type", type: "text", placeholder: "Enter event type", required: false },
          { name: "content", label: "Content", type: "textarea", placeholder: "Enter content", required: false },
        ],
        grants: [
          { name: "grant_name", label: "Grant Name", type: "text", placeholder: "Enter grant name", required: true },
          { name: "purpose", label: "Purpose", type: "textarea", placeholder: "Enter purpose", required: true },
          { name: "amount", label: "Amount", type: "number", placeholder: "Enter amount", required: true },
          { name: "frequency", label: "Frequency", type: "text", placeholder: "Enter frequency", required: true },
          { name: "start_date", label: "Start Date", type: "date", placeholder: "Enter start date", required: true },
          { name: "end_date", label: "End Date", type: "date", placeholder: "Enter end date", required: false },
        ],
      };
      this.fields = modulesConfig[this.selectedModule] || [];
      this.formData = {};
      this.fields.forEach((field) => {
        this.formData[field.name] = ""; // Initialize fields
      });
    },
    // Submit the form data to the backend
    async submitData() {
      try {
        const response = await axios.post(
          `http://127.0.0.1:5000/${this.selectedModule}/`,
          this.formData
        );
        console.log("Server response:", response.data);
        alert("Data added successfully!");
        this.formData = {};
      } catch (error) {
        console.error("Failed to add data:", error);
        alert("Failed to add data.");
      }
    },
  },
};
</script>

<style scoped>
/* Container for the entire Add Data page */
.add-data-container {
  max-width: 800px;
  margin: 100px auto 20px auto; /* Center and leave space from top */
  padding: 20px;
  box-sizing: border-box;
  background-color: #f7f9fa; /* Light background for a softer look */
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

/* Page title styling */
.add-data-container h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
  font-size: 28px;
}

/* Module selector styles */
.module-selector {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
  font-family: Arial, sans-serif;
}

.module-selector label {
  margin-bottom: 8px;
  font-weight: bold;
  color: #34495e;
}

.module-selector select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

/* Form container and groups */
.data-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  margin-bottom: 6px;
  font-weight: bold;
  font-family: Arial, sans-serif;
  color: #34495e;
}

.form-input-wrapper {
  display: flex;
  flex-direction: column;
}

.form-input, .form-textarea {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-family: Arial, sans-serif;
  font-size: 14px;
}

.form-input:focus, .form-textarea:focus,
.module-selector select:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 3px rgba(66, 185, 131, 0.3);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

/* Submit button styling */
.submit-button {
  align-self: flex-start;
  padding: 10px 20px;
  background-color: #42b983;
  color: #fff;
  font-weight: bold;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-family: Arial, sans-serif;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #36a778;
}

/* Responsive design */
@media (max-width: 600px) {
  .add-data-container {
    margin: 60px auto 20px auto;
    padding: 15px;
  }

  .form-group {
    gap: 10px;
  }

  .form-input, .form-textarea, .module-selector select {
    font-size: 14px;
  }
}
</style>
