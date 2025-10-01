import { Grid, Box, Button, Typography } from '@mui/material';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import AddIcon from '@mui/icons-material/Add';
import NotificationsIcon from '@mui/icons-material/Notifications';

function MyGridComponent() {
  return (
    // Use Grid as the container
    <Grid container spacing={2}> {/* spacing prop adds the gap */}
      
      {/* Grid item 1: 6 of 12 columns = 50% */}
      <Grid size={{xs:6}}>
        <Box display="flex" sx={{ border: '1px solid #ccc', p: 2, borderRadius: 1, alignItems: 'center', width: '100%' }}>
          <Box sx={{ mr: 2 }}>
            <CalendarTodayIcon />
          </Box>
          <Box flexGrow="1">
            <Typography>Upcoming Events</Typography>
          </Box>
          <Box>
            <Button variant="outlined" startIcon={<AddIcon />}>
              Create Events
            </Button>
          </Box>
        </Box>
      </Grid>

      {/* Grid item 2: 6 of 12 columns = 50% */}
      <Grid size={{xs:6}}>
        <Box display="flex" sx={{ border: '1px solid #ccc', p: 2, borderRadius: 1, alignItems: 'center', width: '100%' }}>
          <Box sx={{ mr: 2 }}>
            <NotificationsIcon />
          </Box>
          <Box flexGrow="1">
            <Typography>Recent Announcement</Typography>
          </Box>
          <Box>
            <Button variant="outlined" startIcon={<AddIcon />}>
              Create Announcement
            </Button>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
}
export default MyGridComponent;