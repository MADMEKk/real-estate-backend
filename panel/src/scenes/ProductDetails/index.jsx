import React, { useEffect, useState } from "react";
import {
    Box,
    Button,
    Container, Dialog, DialogActions, DialogContent, DialogTitle,
    Divider,
    FormControl, FormControlLabel, FormLabel,
    Grid, Radio, RadioGroup,
    TextField,
    useTheme
} from "@mui/material";

import ProductDetailsSkelton from "components/ProductDetailsSkelton";
import ProductDetailSlider from "components/ProductDetailSlider";
import { useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { getPropertyBySlug, updateProperty } from "../../features/properties/propertyDetailsSlice";
import ProductForm from "../../components/ProductForm";

const ProductDetails = () => {
    const { slug } = useParams();
    const theme = useTheme();
    const dispatch = useDispatch();
    const { property, isLoading } = useSelector((state) => state.property);
    const [editedProperty, setEditedProperty] = useState(null);
    const [openEditDialog, setOpenEditDialog] = useState(false);
    useEffect(() => {
        dispatch(getPropertyBySlug(slug)); // Fetch property details when component mounts
    }, [dispatch, slug]);

    useEffect(() => {
        setEditedProperty(property); // Set initial state for editing
    }, [property]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setEditedProperty({ ...editedProperty, [name]: value });
    };
    const handleRadioChange = (e) => {
        const { name, value } = e.target;
        setEditedProperty({ ...editedProperty, [name]: value === "yes" });
    };
    const handleUpdate = () => {
        dispatch(updateProperty(editedProperty)); // Dispatch update action
    };

    return (
        <>
            {isLoading ? (
                <ProductDetailsSkelton />
            ) : (
                <>
                    <Container>
                        <Grid container spacing={2}>
                            <Grid item xs={12} md={7}>
                                <Box sx={{ mt: 5 }}>
                                    <ProductDetailSlider property={property} />
                                </Box>
                            </Grid>
                            <Grid item xs={12} md={5}>

                                <div className="product-details">
                                    <h2>Edit Product</h2>
                                    <Button onClick={() => setOpenEditDialog(true)} style={{ color: 'white' , background : 'tan' }}>Edit</Button>
                                </div>


                            </Grid>
                        </Grid>
                    </Container>

                    <Dialog open={openEditDialog} onClose={() => setOpenEditDialog(false)}>
                        <DialogTitle>Edit Product</DialogTitle>
                        <DialogContent>
                            <ProductForm
                                editedProperty={editedProperty}
                                handleInputChange={handleInputChange}
                                handleRadioChange={handleRadioChange}
                                handleUpdate={handleUpdate}
                            />
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={() => setOpenEditDialog(false)}>Cancel</Button>
                        </DialogActions>
                    </Dialog>
                </>
            )}
        </>
    );
};

export default ProductDetails;
