import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {getPropertyDetails, getPropertyPhotos, updatePropertyapi} from "./propertyDetailsAPIServices";

const initialState = {
    property: null,
    isLoading: false,
    isError: false,
};

export const updateProperty = createAsyncThunk(
    "property/update",
    async (updatedProperty, { rejectWithValue }) => {
        try {
            return await updatePropertyapi(updatedProperty);
        } catch (error) {
            return rejectWithValue(error.message || "Failed to update property");
        }
    }
);

export const getPropertyBySlug = createAsyncThunk(
    "property/getBySlug",
    async (slug, { rejectWithValue }) => {
        try {
            const property = await getPropertyDetails(slug);
            property.photos = await getPropertyPhotos(slug);
            return property;
        } catch (error) {
            return rejectWithValue(error.message || "Failed to fetch property details");
        }
    }
);

const propertyDetailsSlice = createSlice({
    name: "property",
    initialState,
    reducers: {
        resetProperty: (state) => {
            state.property = null;
            state.isLoading = false;
            state.isError = false;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(getPropertyBySlug.pending, (state) => {
                state.isLoading = true;
                state.isError = false; // Reset isError state when fetching starts
            })
            .addCase(getPropertyBySlug.fulfilled, (state, action) => {
                state.isLoading = false;
                state.property = action.payload;
            })
            .addCase(getPropertyBySlug.rejected, (state) => {
                state.isLoading = false;
                state.isError = true;
            })
            .addCase(updateProperty.pending, (state) => {
                state.isLoading = true;
                state.isError = false; // Reset isError state when updating starts
            })
            .addCase(updateProperty.fulfilled, (state, action) => {
                state.isLoading = false;
                state.property = action.payload;
            })
            .addCase(updateProperty.rejected, (state, action) => {
                state.isLoading = false;
                state.isError = true;
            });
    },
});

export const { resetProperty } = propertyDetailsSlice.actions;
export default propertyDetailsSlice.reducer;
