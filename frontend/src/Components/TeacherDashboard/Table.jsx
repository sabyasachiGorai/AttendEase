import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Chip,
  Stack,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination
} from '@mui/material';
import {
  ArrowDownward as ArrowDownwardIcon,
  ArrowUpward as ArrowUpwardIcon,
  Remove as RemoveIcon, // Represents neutral trend
} from '@mui/icons-material';

// Dummy data
// Will replace this once backend is complete.
const dummyStudents = [
  { id: 1, name: 'Alex Johnson', attendanceRate: 68, consecutiveAbsences: 3, trend: 'down' },
  { id: 2, name: 'Maya Patel', attendanceRate: 72, consecutiveAbsences: 0, trend: 'up' },
  { id: 3, name: 'James Wilson', attendanceRate: 65, consecutiveAbsences: 2, trend: 'down' },
  { id: 4, name: 'Priya Singh', attendanceRate: 95, consecutiveAbsences: 0, trend: 'up' },
  { id: 5, name: 'Ben Carter', attendanceRate: 81, consecutiveAbsences: 0, trend: 'neutral' },
  { id: 6, name: 'Olivia Chen', attendanceRate: 75, consecutiveAbsences: 1, trend: 'neutral' },
  { id: 7, name: 'Liam Garcia', attendanceRate: 55, consecutiveAbsences: 5, trend: 'down' },
  { id: 8, name: 'Sophia Rodriguez', attendanceRate: 58, consecutiveAbsences: 4, trend: 'down' },
  { id: 9, name: 'Noah Martinez', attendanceRate: 62, consecutiveAbsences: 3, trend: 'down' },
  { id: 10, name: 'Isabella Lee', attendanceRate: 98, consecutiveAbsences: 0, trend: 'up' },
  { id: 11, name: 'William Kim', attendanceRate: 78, consecutiveAbsences: 0, trend: 'neutral' },
  { id: 12, name: 'Ava Brown', attendanceRate: 88, consecutiveAbsences: 0, trend: 'up' },
  { id: 13, name: 'Michael Nguyen', attendanceRate: 71, consecutiveAbsences: 1, trend: 'neutral' },
  { id: 14, name: 'Emma Davis', attendanceRate: 69, consecutiveAbsences: 2, trend: 'down' },
];


// Helper function to get the right styles based on student data
const getAttendanceStyles = (rate) => {
  if (rate < 70) {
    return { color: '#f44336', dotBg: '#f44336' }; // Red
  }
  if (rate < 80) {
    return { color: '#ff9800', dotBg: '#ff9800' }; // Orange
  }
  return { color: '#4caf50', dotBg: '#4caf50' }; // Green
};

const TrendIcon = ({ trend }) => {
  switch (trend) {
    case 'up':
      return <ArrowUpwardIcon sx={{ color: 'success.main', verticalAlign: 'middle' }} />;
    case 'down':
      return <ArrowDownwardIcon sx={{ color: 'error.main', verticalAlign: 'middle' }} />;
    default:
      return <RemoveIcon sx={{ color: 'text.disabled', verticalAlign: 'middle' }} />;
  }
};

// --- Main Component ---
function StudentAttendanceList() {
  const [students, setStudents] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };


  React.useEffect(() => {
    // --- BACKEND DATA FETCHING LOGIC ---
    // 1. When your backend is ready, uncomment this section.
    /*
    const fetchStudents = async () => {
      try {
        setLoading(true);
        const response = await fetch('https://your-api.com/students/attendance');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setStudents(data);
      } catch (error) {
        console.error("Failed to fetch students:", error);
        // Optionally, set an error state to display a message to the user
      } finally {
        setLoading(false);
      }
    };
    
    fetchStudents();
    */

    // 2. For now, we use dummy data with a simulated delay.
    //    Remove this part when you uncomment the fetch logic above.
    const timer = setTimeout(() => {
      setStudents(dummyStudents);
      setLoading(false);
    }, 1500); // Simulate network delay

    return () => clearTimeout(timer); // Cleanup timer on unmount
  }, []);


  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper sx={{ width: '100%', overflow: 'hidden', borderRadius: '12px' }}>
      <TableContainer sx={{ maxHeight: 440 }}>
        <Table stickyHeader aria-label="student attendance table">
          <TableHead>
            <TableRow sx={{
                backgroundColor: "grey.100"
            }}>
              <TableCell sx={{ fontWeight: 'bold' }}>Student Name</TableCell>
              <TableCell sx={{ fontWeight: 'bold' }}>Attendance Rate</TableCell>
              <TableCell sx={{ fontWeight: 'bold' }}>Status</TableCell>
              <TableCell align="right" sx={{ fontWeight: 'bold' }}>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {students
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((student) => {
                const { dotBg } = getAttendanceStyles(student.attendanceRate);
                return (
                  <TableRow
                    hover
                    role="checkbox"
                    tabIndex={-1}
                    key={student.id}
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                  >
                    <TableCell component="th" scope="row">
                      <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                        {student.name}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Stack direction="row" alignItems="center" spacing={1.5}>
                        <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: dotBg }} />
                        <Typography variant="body2" color="text.secondary">
                          {student.attendanceRate}%
                        </Typography>
                      </Stack>
                    </TableCell>
                    <TableCell>
                      {student.consecutiveAbsences > 0 ? (
                         <Chip
                            label={`${student.consecutiveAbsences} consecutive absences`}
                            color="error"
                            size="small"
                            sx={{ backgroundColor: '#ffebee', color: '#c62828', fontWeight: 'medium' }}
                         />
                      ) : (
                        <Typography variant="body2" color="text.secondary">-</Typography>
                      )}
                    </TableCell>
                    <TableCell align="right">
                        <Stack direction="row" alignItems="center" justifyContent="flex-end" spacing={1}>
                            <TrendIcon trend={student.trend} />
                            <Button variant="outlined" size="small" sx={{ borderRadius: '20px', textTransform: 'none' }}>
                                Contact
                            </Button>
                        </Stack>
                    </TableCell>
                  </TableRow>
                );
              })}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[10, 25, 100]}
        component="div"
        count={students.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Paper>
  );
}

export default StudentAttendanceList;


