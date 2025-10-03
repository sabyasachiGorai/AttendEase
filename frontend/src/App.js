import { useState, useEffect } from "react";
import axios from "axios";

const API_BASE = "https://friendly-guide-qr476x9xwrjhx6qq-8000.app.github.dev/";

function App() {
  const [students, setStudents] = useState([]);
  const [form, setForm] = useState({
    name: "",
    email: "",
    roll_number: "",
    attendance_percentage: ""
  });

  // Fetch students
  const fetchStudents = async () => {
    const res = await axios.get(API_BASE);
    setStudents(res.data);
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  // Handle form change
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Handle form submit
  const handleSubmit = async (e) => {
    e.preventDefault();
    await axios.post(API_BASE, {
      name: form.name,
      email: form.email,
      roll_number: form.roll_number,
      attendance_percentage: parseFloat(form.attendance_percentage)
    });
    setForm({ name: "", email: "", roll_number: "", attendance_percentage: "" });
    fetchStudents();
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>AttendEase - Students</h1>

      <h2>Add Student</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: "2rem" }}>
        <input name="name" placeholder="Name" value={form.name} onChange={handleChange} required />
        <input name="email" placeholder="Email" value={form.email} onChange={handleChange} required />
        <input name="roll_number" placeholder="Roll Number" value={form.roll_number} onChange={handleChange} required />
        <input
          name="attendance_percentage"
          placeholder="Attendance %"
          type="number"
          step="0.01"
          value={form.attendance_percentage}
          onChange={handleChange}
          required
        />
        <button type="submit">Add Student</button>
      </form>

      <h2>All Students</h2>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Roll Number</th>
            <th>Name</th>
            <th>Email</th>
            <th>Attendance %</th>
          </tr>
        </thead>
        <tbody>
          {students.map((s) => (
            <tr key={s.id}>
              <td>{s.roll_number}</td>
              <td>{s.name}</td>
              <td>{s.email}</td>
              <td>{s.attendance_percentage}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
