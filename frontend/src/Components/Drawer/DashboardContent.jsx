import * as React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Alert from "@mui/material/Alert";
import AlertTitle from "@mui/material/AlertTitle";
import { styled } from "@mui/material/styles";

// Import your custom components
import CustomCircularProgress from "./TeacherDashboard/CustomCircularProgress";
import StudentAttendanceList from "./TeacherDashboard/Table";
import MyGridComponent from "./TeacherDashboard/MyGridComponent";
import FrontCards from "./TeacherDashboard/FrontCards";

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "flex-end",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
}));

export default function DashboardContent() {
  const [alertOpen, setAlertOpen] = React.useState(true);

  return (
    <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
      <DrawerHeader />
      {/* Welcome Message and Stat Cards */}
      <Typography variant="h5">
        Welcome back,{"{"}Mohd, Waris{"}"}
      </Typography>
      {/* //Cards to show the total number of students and other things  */}
      <FrontCards />

      {/* Low Attendance Warning */}
      <Box sx={{ my: 2 }}>
        {alertOpen && (
          <Alert severity="warning" onClose={() => setAlertOpen(false)}>
            <AlertTitle>Low Attendance Alert</AlertTitle>
            Some students have low attendance. Check the list below.
          </Alert>
        )}
      </Box>

      {/* Attendance Charts and Lists */}
      <Box display="flex" gap={2} sx={{ my: 2 }}>
        {/* Today's Attendance Summary Box */}
        <Box flex={1}>
          <Typography>Today's Attendance Summary</Typography>
          <Typography>
            Class-{"{"}
            {"}"} Subject-{"{"}
            {"}"}{" "}
          </Typography>
          <Box>
            <CustomCircularProgress value={50} label="Present Today" />
          </Box>
          {/* ... other summary details */}

          <Box display="flex">
            <Box>
              <Typography>This Week</Typography>
              <Typography>
                {"{"}Percentage{"}"}
              </Typography>
            </Box>
            <Box>
              <Typography>This Month</Typography>
              <Typography>
                {"{"}Percentage{"}"}
              </Typography>
            </Box>
          </Box>
        </Box>
        {/* Short Attendance Students Box */}
        <Box flex={1}>
          <Alert severity="error">Students with less than 75% attendance</Alert>
          <StudentAttendanceList />
        </Box>
      </Box>

      {/* Events and Announcements */}
      <MyGridComponent />
    </Box>
  );
}
