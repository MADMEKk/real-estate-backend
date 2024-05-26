import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Box, useTheme, Button, Table, TableHead, TableRow, TableCell, TableBody } from "@mui/material";
import { getProperties, reset } from "../../features/properties/propertySlice";
import Header from "../../components/Header";
import ProductTableRow from "../../components/ProductTableRow";
import { publishProperty, unpublishProperty } from "../../features/properties/propertySlice";

const Transactions = () => {
    const theme = useTheme();
    const dispatch = useDispatch();
    const { properties: allProperties = [], isLoading } = useSelector((state) => state.properties); // Set default value for allProperties
    const [unpublishedOnly, setUnpublishedOnly] = useState(false);

    // Filter properties based on unpublishedOnly state
    const properties = unpublishedOnly ? allProperties.filter(property => !property.published_status) : allProperties;

    useEffect(() => {
        // Fetch properties initially
        dispatch(getProperties());

        return () => {
            dispatch(reset());
        };
    }, [dispatch]); // Only run when dispatch changes

    const handleToggleUnpublished = () => {
        setUnpublishedOnly(!unpublishedOnly);
    };

    const columns = [
        { id: "_id", label: "ID", minWidth: 100 },
        { id: "user", label: "User", minWidth: 100 },
        { id: "createdAt", label: "Created At", minWidth: 100 },
        { id: "price", label: "Price", minWidth: 100 },
        { id: "bedrooms", label: "Bedrooms", minWidth: 100 },
        { id: "bathrooms", label: "Bathrooms", minWidth: 100 },
        { id: "advert_type", label: "Advert Type", minWidth: 100 },
        { id: "property_type", label: "Property Type", minWidth: 100 },
        { id: "actions", label: "Actions", minWidth: 100 },
    ];

    const handlePublishProperty = async (propertyId) => {
        try {
            await dispatch(publishProperty(propertyId));
            // Dispatch getProperties to refresh state after successful publish
            dispatch(getProperties());
        } catch (error) {
            console.error("Error publishing property:", error);
            // Handle publish error (optional: display error message to user)
        }
    };

    const handleUnpublishProperty = async (propertyId) => {
        try {
            await dispatch(unpublishProperty(propertyId));
            // Dispatch getProperties to refresh state after successful unpublish
            dispatch(getProperties());
        } catch (error) {
            console.error("Error unpublishing property:", error);
            // Handle unpublish error (optional: display error message to user)
        }
    };

    return (
        <Box m="1.5rem 2.5rem">
            <Header title="TRANSACTIONS" subtitle="Entire list of transactions" />
            {properties || !isLoading ? ( // Check if properties exist or data isn't loading
                <Box
                    height="80vh"
                    sx={{
                        "& .MuiDataGrid-root": {
                            border: "none",
                        },
                        "& .MuiDataGrid-cell": {
                            borderBottom: "none",
                        },
                        "& .MuiDataGrid-columnHeaders": {
                            backgroundColor: theme.palette.background.alt,
                            color: theme.palette.secondary[100],
                            borderBottom: "none",
                        },
                        "& .MuiDataGrid-virtualScroller": {
                            backgroundColor: theme.palette.primary.light,
                        },
                        "& .MuiDataGrid-footerContainer": {
                            backgroundColor: theme.palette.background.alt,
                            color: theme.palette.secondary[100],
                            borderTop: "none",
                        },
                        "& .MuiDataGrid-toolbarContainer .MuiButton-text": {
                            color: `${theme.palette.secondary[200]} !important`,
                        },
                    }}
                >
                    <Button onClick={handleToggleUnpublished} variant="outlined" color="primary" sx={{ mb: 2 }}>
                        {unpublishedOnly ? "Show All Properties" : "Show Unpublished Only"}
                    </Button>
                    <Table stickyHeader>
                        <TableHead>
                            <TableRow>
                                {columns.map((column) => (
                                    <TableCell key={column.id} style={{ minWidth: column.minWidth }}>
                                        {column.label}
                                    </TableCell>
                                ))}                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {properties.map((property) => (
                                <ProductTableRow
                                    key={property.slug}
                                    property={property}
                                    onPublish={handlePublishProperty}
                                    onUnpublish={handleUnpublishProperty}
                                />
                            ))}
                        </TableBody>
                    </Table>
                </Box>
            ) : (
                <>Loading...</>
            )}
        </Box>
    );
};

export default Transactions;
