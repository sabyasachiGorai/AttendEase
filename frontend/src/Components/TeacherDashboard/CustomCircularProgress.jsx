import CircularProgress from '@mui/material/CircularProgress';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { green } from '@mui/material/colors';

function CustomCircularProgress(props) {
  // Destructure props with default values
  const { value = 0, label = "Present Today", size = 120, thickness = 4 } = props;

  return (
    <Box sx={{ position: 'relative', display: 'inline-flex' }}>
      {/* Background Track */}
      <CircularProgress
        variant="determinate"
        sx={{
          color: (theme) => theme.palette.grey[200],
        }}
        size={size}
        thickness={thickness}
        value={100}
      />
      {/* Foreground Progress Arc */}
      <CircularProgress
        variant="determinate"
        value={value}
        sx={{
          color: green[500],
          position: 'absolute',
          left: 0,
          // Add a smooth transition
          transition: 'transform 0.4s ease-in-out',
        }}
        size={size}
        thickness={thickness}
      />
      {/* Centered Text */}
      <Box
        sx={{
          top: 0,
          left: 0,
          bottom: 0,
          right: 0,
          position: 'absolute',
          display: 'flex',
          flexDirection: 'column', // Stack text vertically
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Typography 
          variant="h5" 
          component="div" 
          color="text.primary" 
          sx={{ fontWeight: 'bold' }}
        >
          {`${Math.round(value)}%`}
        </Typography>
        <Typography 
          variant="caption" 
          component="div" 
          color="text.secondary"
        >
          {label}
        </Typography>
      </Box>
    </Box>
  );
}

export default CustomCircularProgress;