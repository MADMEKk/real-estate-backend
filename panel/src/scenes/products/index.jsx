import React, {useEffect, useState} from "react";
import {useDispatch, useSelector} from "react-redux";
import {getProperties} from "../../features/properties/propertySlice";

import {
  Box,
  Card,
  CardActions,
  CardContent,
  Collapse,
  Button,
  Typography,
  Rating,
  useTheme,
  useMediaQuery, CardMedia, IconButton, Link,
} from "@mui/material";
import Header from "../../components/Header";
import {Bathtub, Expand, ExpandMore, Favorite, LocalHotel, Share} from "@mui/icons-material";
import {useLocation, useNavigate} from "react-router-dom";

const Product = ({ property }) => {
  const theme = useTheme();
  const [isExpanded, setIsExpanded] = useState(false);
  function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }
  const navigate = useNavigate();
  const { pathname } = useLocation();
    const trimmedPathname = pathname.replace("/All Properies", "");

    const productDetailsLink = `${trimmedPathname}/product/${property.slug}`;
  return (
    <Card
      sx={{
        backgroundImage: "none",
        backgroundColor: theme.palette.background.alt,
        borderRadius: "0.55rem",
      }}
    >

        {/* Your content here */}

  <Link
      to={productDetailsLink}
      onClick={() => {
        navigate(productDetailsLink); // Redirect to the product details page
      }}
  >        <CardMedia
            component="img"
            height="194"
            image={property.cover_photo}
            alt="Paella dish"
        />
      </Link>
      <CardContent>
        <Typography
          sx={{ fontSize: 14 }}
          color={theme.palette.secondary[700]}
          gutterBottom
        >
          {property.advert_type}
        </Typography>
        <Typography variant="h5" component="div">
          {property.title}
        </Typography>
        <Typography sx={{ mb: "1.5rem" }} color={theme.palette.secondary[400]}>
        {numberWithCommas(Number(property.price))} DZD
        </Typography>
        <Typography sx={{ mb: "1.5rem" }} color={theme.palette.secondary[400]}>
          {property.city}  / {property.street_address} / {property.property_number}
        </Typography>

        <IconButton aria-label="bathrooms">
          <Bathtub /> {property.bathrooms}
        </IconButton>
        <IconButton aria-label="bedrooms">
          <LocalHotel /> {property.bedrooms}
        </IconButton>
        <IconButton aria-label="area m2">
            <Expand /> {property.plot_area} m²
        </IconButton>


      </CardContent>
      <CardActions>
        <Button
          variant="primary"
          size="small"
          onClick={() => setIsExpanded(!isExpanded)}
        >
         Edit
        </Button>
        <Button
            variant="primary"
            size="small"
            onClick={() => setIsExpanded(!isExpanded)}
        >
          Delete
        </Button>

        <ExpandMore
            expand={isExpanded}
            onClick={() => setIsExpanded(!isExpanded)}
            aria-expanded={isExpanded}
            aria-label="show more"
        >
          <ExpandMore />
        </ExpandMore>
      </CardActions>
      <Collapse
        in={isExpanded}
        timeout="auto"
        unmountOnExit
        sx={{
          color: theme.palette.neutral[300],
        }}
      >
        <CardContent>
          <Typography>id: ${property.slug}</Typography>
          <Typography variant="body2">Description : {property.description.substring(0, 70)}</Typography>


        </CardContent>
      </Collapse>
    </Card>
  );
};

const Products = () => {
  const { properties, isLoading, isSuccess } = useSelector(
      (state) => state.properties
  );
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(getProperties());
  }, [dispatch]);
  const isNonMobile = useMediaQuery("(min-width: 1000px)");

  return (
    <Box m="1.5rem 2.5rem">
      <Header title="PROPERTIES" subtitle="See your list of properties." />
      {properties || !isLoading ? (
        <Box
          mt="20px"
          display="grid"
          gridTemplateColumns="repeat(4, minmax(0, 1fr))"
          justifyContent="space-between"
          rowGap="20px"
          columnGap="1.33%"
          sx={{
            "& > div": { gridColumn: isNonMobile ? undefined : "span 4" },
          }}
        >
          {properties.map(
            (property) => (
              <Product
                  property={property}
              />
            )
          )}
        </Box>
      ) : (
        <>Loading...</>
      )}
    </Box>
  );
};

export default Products;
