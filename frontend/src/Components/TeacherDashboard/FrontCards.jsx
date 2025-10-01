import { Box, Grid, Typography } from "@mui/material";
import PeopleAltIcon from "@mui/icons-material/PeopleAlt";

function FrontCards() {
  return (
    <Grid container spacing={2}>
      <Grid size={{ xs: 3 }}>
        <Box
          display="flex"
          sx={{
            border: "1px solid #ccc",
            p: 2,
            borderRadius: 1,
            alignItems: "center",
            width: "100%",
          }}
        >
          <Box>
            <Typography>Total Students</Typography>
            <Typography>
              {"{"}Number{"}"}
            </Typography>
          </Box>
          <Box>
            <PeopleAltIcon />
          </Box>
        </Box>
      </Grid>
      <Grid size={{ xs: 3 }}>
        <Box
          display="flex"
          sx={{
            border: "1px solid #ccc",
            p: 2,
            borderRadius: 1,
            alignItems: "center",
            width: "100%",
          }}
        >
          <Box>
            <Typography>Total Students</Typography>
            <Typography>
              {"{"}Number{"}"}
            </Typography>
          </Box>
          <Box>
            <PeopleAltIcon />
          </Box>
        </Box>
      </Grid>
      <Grid size={{ xs: 3 }}>
        <Box
          display="flex"
          sx={{
            border: "1px solid #ccc",
            p: 2,
            borderRadius: 1,
            alignItems: "center",
            width: "100%",
          }}
        >
          <Box>
            <Typography>Total Students</Typography>
            <Typography>
              {"{"}Number{"}"}
            </Typography>
          </Box>
          <Box>
            <PeopleAltIcon />
          </Box>
        </Box>
      </Grid>
      <Grid size={{ xs: 3 }}>
        <Box
          display="flex"
          sx={{
            border: "1px solid #ccc",
            p: 2,
            borderRadius: 1,
            alignItems: "center",
            width: "100%",
          }}
        >
          <Box>
            <Typography>Total Students</Typography>
            <Typography>
              {"{"}Number{"}"}
            </Typography>
          </Box>
          <Box>
            <PeopleAltIcon />
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
}
export default FrontCards;