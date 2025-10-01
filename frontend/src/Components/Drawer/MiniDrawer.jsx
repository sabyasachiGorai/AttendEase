import * as React from "react";
import Box from "@mui/material/Box";
import CssBaseline from "@mui/material/CssBaseline";
import TopBar from "./TopBar";
import SideNav from "./SideNav"; 
import DashboardContent from "./DashboardContent"; 

export default function MiniDrawer() {
  const [open, setOpen] = React.useState(true);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <TopBar open={open} handleDrawerOpen={handleDrawerOpen} handleDrawerClose={handleDrawerClose} />
      <SideNav open={open} handleDrawerClose={handleDrawerClose} />
      <DashboardContent />
    </Box>
  );
}