import * as React from "react";
import { styled } from "@mui/material/styles";
import MuiAppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
// import MenuOpenIcon from "@mui/icons-material/MenuOpen";
import Box from "@mui/material/Box";

const drawerWidth = 240;

// Function to display date
function currentDate() {
  const today = new Date();
  return today.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    timeZone: "Asia/Kolkata",
  });
}

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(["width", "margin"], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

export default function TopBar({ open, handleDrawerOpen, handleDrawerClose }) {
  return (
    <AppBar position="fixed" open={open}>
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="toggle drawer"
          onClick={open ? handleDrawerClose : handleDrawerOpen}
          edge="start"
          sx={{ marginRight: 5, ...(open && { display: "none" }) }}
        >
          <MenuIcon />
        </IconButton>
        <Box
          display="flex"
          width="100%"
          justifyContent="space-between"
          alignItems="center"
        >
          <Box display="flex" flexDirection="column">
            <Typography variant="h6" noWrap component="div">
              EduEase
            </Typography>
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
  );
}