import * as React from "react";
import { styled, useTheme } from "@mui/material/styles";
import MuiDrawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Avatar from "@mui/material/Avatar";
// Importing Icons for SideBar in the Drawer
import DashboardIcon from "@mui/icons-material/Dashboard";
import EventAvailableIcon from "@mui/icons-material/EventAvailable";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import ChatBubbleIcon from "@mui/icons-material/ChatBubble";
import GroupIcon from "@mui/icons-material/Group";
import SettingsIcon from "@mui/icons-material/Settings";
import NotificationsIcon from "@mui/icons-material/Notifications";
import LogoutIcon from "@mui/icons-material/Logout";

const drawerWidth = 240;

const openedMixin = (theme) => ({
  //open mixin style
  width: drawerWidth,
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    // duration: theme.transitions.duration.enteringScreen,
    duration: 500,
  }),
  overflowX: "hidden",
});

const closedMixin = (theme) => ({
  // ...closedMixin styles
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

//Verify this again!
const DrawerHeader = styled("div")(({ theme }) => ({
  //DrawerHeader styles
  display: "flex",
  alignItems: "center",
  justifyContent: "flex-end",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar but this thing is not working!
  ...theme.mixins.toolbar,
}));

const Drawer = styled(MuiDrawer, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  width: drawerWidth,
  flexShrink: 0,
  whiteSpace: "nowrap",
  boxSizing: "border-box",
  ...(open && {
    ...openedMixin(theme),
    "& .MuiDrawer-paper": openedMixin(theme),
  }),
  ...(!open && {
    ...closedMixin(theme),
    "& .MuiDrawer-paper": closedMixin(theme),
  }),
}));

export default function SideNav({ open, handleDrawerClose }) {
  const theme = useTheme();
// List of items to be displayed in the drawer component 
  const menuItems = [
    { text: "Dashboard", icon: <DashboardIcon /> },
    { text: "Attendance", icon: <EventAvailableIcon /> },
    { text: "Create Events", icon: <CalendarMonthIcon /> },
    { text: "Events Feed", icon: <ChatBubbleIcon /> },
    { text: "Students", icon: <GroupIcon /> },
  ];
  const menuItems2=[
    { text: "Notifications", icon: <NotificationsIcon /> },
    { text: "Settings", icon: <SettingsIcon /> },
    { text: "Log Out", icon: <LogoutIcon /> },
  ];
  return (
    <Drawer variant="permanent" open={open}>
      <DrawerHeader>
        <IconButton onClick={handleDrawerClose}>
          {theme.direction === "rtl" ? (
            <ChevronRightIcon />
          ) : (
            <ChevronLeftIcon />
          )}
        </IconButton>
      </DrawerHeader>
      <Divider />
      {/* Teacher Info List */}
      <List>
        <ListItem disablePadding>
          <ListItemButton>
            <ListItemIcon>
              <Avatar sx={{ width: 28, height: 28 }} />
            </ListItemIcon>
            <ListItemText primary="Teacher Name" secondary="Teacher Subject" />
          </ListItemButton>
        </ListItem>
      </List>
      <Divider />
      {/* Main Nav List */}
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding sx={{ display: "block" }}>
            <ListItemButton>
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Divider />
      {/* Settings/Logout List */}

      <List>{menuItems2.map((item) => (
          <ListItem key={item.text} disablePadding sx={{ display: "block" }}>
            <ListItemButton>
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}</List>
    </Drawer>
  );
}
