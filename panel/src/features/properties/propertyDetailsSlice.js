import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {
    getPropertyDetails,
    getPropertyPhotos,
    replacePropertyPhotoApi,
    updatePropertyapi,
} from "./propertyDetailsAPIServices";

const initialState = {
    property: null,
    isLoading: false,
    isError: false,
};
export const replacePropertyPhoto = createAsyncThunk(
    "property/replacePhoto",
    async ({ propertyId, photoId, newFile }, { rejectWithValue }) => {
        try {
            const formData = new FormData();
            formData.append('file', newFile);
            const response = await replacePropertyPhotoApi(propertyId, photoId, formData);
            return response.data;
        } catch (error) {
            return rejectWithValue(error.message || "Failed to replace photo");
        }
    }
);
export const updateProperty = createAsyncThunk(
    "property/update",
    async (updatedProperty, { rejectWithValue }) => {
        try {
            const property = await updatePropertyapi(updatedProperty);
            property.photos = await getPropertyPhotos(property.slug);
            return property;
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
            .addCase(replacePropertyPhoto.fulfilled, (state, action) => {
                const updatedPhotos = state.property.photos.map(photo =>
                    photo.id === action.payload.id ? action.payload : photo
                );
                state.property.photos = updatedPhotos;
            })
            .addCase(updateProperty.rejected, (state, action) => {
                state.isLoading = false;
                state.isError = true;
            });
    },
});

export const { resetProperty } = propertyDetailsSlice.actions;
export default propertyDetailsSlice.reducer;
