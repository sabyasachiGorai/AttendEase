import * as React from "react";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import MuiDrawer from "@mui/material/Drawer";
import MuiAppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import CssBaseline from "@mui/material/CssBaseline";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import MenuOpenIcon from "@mui/icons-material/MenuOpen";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import LogoutIcon from "@mui/icons-material/Logout";
import DashboardIcon from "@mui/icons-material/Dashboard";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import EventAvailableIcon from "@mui/icons-material/EventAvailable";
import ChatBubbleIcon from "@mui/icons-material/ChatBubble";
import GroupIcon from "@mui/icons-material/Group";
import SettingsIcon from "@mui/icons-material/Settings";
import NotificationsIcon from "@mui/icons-material/Notifications";
import Avatar from "@mui/material/Avatar";
import { AlertTitle, Button, Paper } from "@mui/material";
import Alert from "@mui/material/Alert";
import Stack from "@mui/material/Stack";
import CustomCircularProgress from "../TeacherDashboard/CustomCircularProgress";
import StudentAttendanceList from "../TeacherDashboard/Table";
import MyGridComponent from "../TeacherDashboard/MyGridComponent";
import FrontCards from "../TeacherDashboard/FrontCards";

const drawerWidth = 240;

// Function to disaplay date
function currentDate() {
  const today = new Date();
  return today.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    timeZone: "Asia/Kolkata",
  });
}

//Item used in the grid
const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: "#fff",
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: "center",
  color: (theme.vars ?? theme).palette.text.secondary,
  ...theme.applyStyles("dark", {
    backgroundColor: "#1A2027",
  }),
}));

//Drawer sliding open
const openedMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    // duration: theme.transitions.duration.enteringScreen,
    duration: 500,
  }),
  overflowX: "hidden",
});

//Drawer sliding closed
const closedMixin = (theme) => ({
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    // duration: theme.transitions.duration.leavingScreen,
    duration: 500,
  }),
  overflowX: "hidden",
  width: `calc(${theme.spacing(7)} + 1px)`,
  [theme.breakpoints.up("sm")]: {
    width: `calc(${theme.spacing(8)} + 1px)`,
  },
});

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "flex-end",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
}));

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(["width", "margin"], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  variants: [
    {
      props: ({ open }) => open,
      style: {
        marginLeft: drawerWidth,
        width: `calc(100% - ${drawerWidth}px)`,
        transition: theme.transitions.create(["width", "margin"], {
          easing: theme.transitions.easing.sharp,
          duration: theme.transitions.duration.enteringScreen,
          // duration:2000
        }),
      },
    },
  ],
}));

const Drawer = styled(MuiDrawer, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme }) => ({
  width: drawerWidth,
  flexShrink: 0,
  whiteSpace: "nowrap",
  boxSizing: "border-box",
  variants: [
    {
      props: ({ open }) => open,
      style: {
        ...openedMixin(theme),
        "& .MuiDrawer-paper": openedMixin(theme),
      },
    },
    {
      props: ({ open }) => !open,
      style: {
        ...closedMixin(theme),
        "& .MuiDrawer-paper": closedMixin(theme),
      },
    },
  ],
}));

export default function MiniDrawer() {
  const theme = useTheme();
  const [open, setOpen] = React.useState(true);
  const [alertOpen, setAlertOpen] = React.useState(true);

  function handleCloseAlert(setter) {
    setter(false);
  }
  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="toggle drawer"
            onClick={open ? handleDrawerClose : handleDrawerOpen}
            edge="start"
            sx={{ marginRight: 3 }}
          >
            {open ? <MenuOpenIcon /> : <MenuIcon />}
          </IconButton>
          <Box
            display="flex"
            width="100%"
            justifyContent="space-between"
            alignItems="center"
          >
            <Box display="flex" flexDirection="column">
              <Typography variant="body1">EduEase</Typography>
              <Typography variant="body2" color="text.secondary">
                Teacher's Dashboard
              </Typography>
            </Box>
            <Box display="flex">
              <Typography sx={{ mr: 1 }} color="text.secondary">
                Today:{" "}
              </Typography>
              <Typography>{currentDate()}</Typography>
            </Box>
          </Box>
        </Toolbar>
      </AppBar>
      <Drawer variant="permanent" open={open}>
        <DrawerHeader>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === "rtl" ? <MenuOpenIcon /> : <MenuIcon />}
          </IconButton>
        </DrawerHeader>

        {/* The list of items in the dashboard  */}
        <Divider />
        <List>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                <Avatar sx={{ width: 28, height: 28 }} />
              </ListItemIcon>
              <ListItemText
                primary="Teacher Name"
                secondary="Teacher Subject"
              />
            </ListItemButton>
          </ListItem>
        </List>
        <Divider></Divider>
        <List>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                <DashboardIcon />
              </ListItemIcon>
              <ListItemText primary="Dashboard" />
            </ListItemButton>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                <EventAvailableIcon />
              </ListItemIcon>
              <ListItemText primary="Attendance" />
            </ListItemButton>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                <CalendarMonthIcon />
              </ListItemIcon>
              <ListItemText primary="Create Events" />
            </ListItemButton>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                <ChatBubbleIcon />
              </ListItemIcon>
              <ListItemText primary="Events Feed" />
            </ListItemButton>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                <GroupIcon />
              </ListItemIcon>
              <ListItemText primary="Students" />
            </ListItemButton>
          </ListItem>
        </List>
        <Divider />
        <List>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                <NotificationsIcon />
              </ListItemIcon>
              <ListItemText primary="Notifications" />
            </ListItemButton>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                <SettingsIcon />
              </ListItemIcon>
              <ListItemText primary="Settings" />
            </ListItemButton>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemIcon>
                <LogoutIcon />
              </ListItemIcon>
              <ListItemText primary="Log Out" />
            </ListItemButton>
          </ListItem>
        </List>
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, pl: 2 }}>
        {/* <DrawerHeader /> */}
        <Box sx={{ mr: 2 }}>
          {/* Upper welcome back  */}
          <Typography>
            Welcome back,{"{"}Mohd, Waris{"}"}
          </Typography>
          {/* Data display box  */}
          <FrontCards />
          {/* Warining box needs automation  */}
          <Box>
            <Stack sx={{ width: "100%" }} spacing={2}>
              {alertOpen && (
                <Alert
                  severity="warning"
                  onClose={() => handleCloseAlert(setAlertOpen)}
                >
                  <AlertTitle>Low Attendance Alert</AlertTitle>
                  This alert displays the default close icon.
                </Alert>
              )}
            </Stack>
          </Box>
        </Box>
        {/* Chart box  */}
        <Box display="flex">
          <Box>
            <Box>
              <Typography>Today's Attendance Summary</Typography>
              <Typography>
                Class-{"{"}
                {"}"} Subject-{"{"}
                {"}"}{" "}
              </Typography>
            </Box>
            <Box>
              <CustomCircularProgress value={50} label="Present Today" />
            </Box>
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
          {/* Short attendance students table with alert message */}
          <Box sx={{ flexGrow: 1, mr: 2 }}>
            <Stack sx={{ width: "100%" }} spacing={2}>
              <Alert severity="error">This is an error Alert.</Alert>
            </Stack>

            <StudentAttendanceList />
          </Box>
        </Box>
        {/* For creating events and announcements */}
        <MyGridComponent />
      </Box>
    </Box>
  );
}
