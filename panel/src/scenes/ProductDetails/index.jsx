


    import React, { useEffect, useState } from "react";
    import {
        Box,
        Button,
        Container,
        Dialog,
        DialogActions,
        DialogContent,
        DialogTitle,
        Divider,
        Grid,
        Typography,
        useTheme
    } from "@mui/material";
    import { useParams } from "react-router-dom";
    import { useDispatch, useSelector } from "react-redux";
    import {getPropertyBySlug, replacePropertyPhoto, updateProperty} from "../../features/properties/propertyDetailsSlice";
    import ProductForm from "../../components/ProductForm";
    import ProductDetailSlider from "../../components/ProductDetailSlider";
    import PhotoEditDialog from "../../components/PhotoEditDialog";
    import ProductDetailsSkelton from "../../components/ProductDetailsSkelton";
    const ProductDetails = () => {
        const { slug } = useParams();
        const theme = useTheme();
        const dispatch = useDispatch();
        const { property, isLoading } = useSelector((state) => state.property);
        const [editedProperty, setEditedProperty] = useState(null);
        const [openEditDialog, setOpenEditDialog] = useState(false);
        const [openPhotoDialog, setOpenPhotoDialog] = useState(false);
        const [selectedPhoto, setSelectedPhoto] = useState(null);
        const [photos, setPhotos] = useState([]);
        const [coverPhoto, setCoverPhoto] = useState(null);
        const [video, setVideo] = useState(null);
        useEffect(() => {
            if (property) {
                const { photos, cover_photo, vedio, ...rest } = property;
                setEditedProperty(rest);
                setPhotos(photos || []);
                setCoverPhoto(cover_photo);
                setVideo(vedio);
            }
        }, [property]);

        useEffect(() => {
            dispatch(getPropertyBySlug(slug));
        }, [dispatch, slug]);

        useEffect(() => {
            if (property) {
                const { photos, cover_photo, vedio, ...rest } = property;
                setEditedProperty(rest);
            }
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
            dispatch(updateProperty(editedProperty));
            setOpenEditDialog(false);
        };

        const handleDelete = () => {
            // Implement delete functionality
            console.log("Delete property");
        };

        if (isLoading) {
            return <div>Loading...</div>;
        }

        if (!property) {
            return <div>Property not found</div>;
        }

    const handlePhotoClick = (photo) => {
        setSelectedPhoto(photo);
        setOpenPhotoDialog(true);
    };


        const handlePhotoDelete = (photoId) => {
            const updatedPhotos = photos.filter(photo => photo.id !== photoId);
            setPhotos(updatedPhotos);
            dispatch(/*deletePropertyPhoto({ propertyId: property.id, photoId })*/)
                .then(() => {
                    // Handle success
                })
                .catch(error => {
                    console.error('Failed to delete photo:', error);
                });
        };
        const handlePhotoReplace = (photoId, newFile) => {
            const updatedPhotos = photos.map(photo =>
                photo.id === photoId ? { ...photo, file: newFile, url: URL.createObjectURL(newFile) } : photo
            );

            setPhotos(updatedPhotos);
            dispatch(replacePropertyPhoto({ propertyId: property.slug, photoId, newFile }))
                .then((action) => {
                    if (!action.error) {
                        // Update local state with new photos if needed
                        setSelectedPhoto(null);                    }
                })
                .catch(error => {
                    console.error('Failed to replace photo:', error);
                });
            setOpenPhotoDialog(false);

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
                                <ProductDetailSlider photos={property.photos} onPhotoClick={handlePhotoClick} />
                            </Box>
                        </Grid>
                        <Grid item xs={12} md={5}>
                            <Box sx={{ mt: 5 }}>
                                <Typography variant="h4">{property.title}</Typography>
                                <Typography variant="subtitle1">{property.description}</Typography>
                                <Divider sx={{ my: 2 }} />
                                <Typography variant="body1">City: {property.city}</Typography>
                                <Typography variant="body1">Price: ${property.price}</Typography>
                                <Typography variant="body1">Bedrooms: {property.bedrooms}</Typography>
                                <Typography variant="body1">Bathrooms: {property.bathrooms}</Typography>
                                <Divider sx={{ my: 2 }} />
                                <Button onClick={() => setOpenEditDialog(true)} variant="contained" color="primary" sx={{ mr: 2 }}>
                                    Edit
                                </Button>
                                <Button onClick={() => setOpenPhotoDialog(true)} variant="contained" color="secondary" sx={{ mr: 2 }}>
                                    Edit Photos
                                </Button>
                                <Button onClick={handleDelete} variant="contained" color="error">
                                    Delete
                                </Button>
                            </Box>
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

                    {selectedPhoto && (
                        <PhotoEditDialog
                            open={openPhotoDialog}
                            onClose={() => setOpenPhotoDialog(false)}
                            photo={selectedPhoto}
                            onDelete={handlePhotoDelete}
                            onReplace={handlePhotoReplace}
                        />
                    )}
                </>
            )}
        </>
    );
};

export default ProductDetails;
