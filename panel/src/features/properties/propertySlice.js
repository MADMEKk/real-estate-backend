import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import propertyAPIService from "./propertyAPIServices"; // Import your property API service
const initialState = {
    properties: [],
    property: {}, // You might not need this depending on your usage
    isError: false,
    isLoading: false,
    isSuccess: false,
    message: "",
};


export const publishProperty = createAsyncThunk(
    "properties/publish",
    async (propertyId) => {
        const response = await propertyAPIService.publishProperty(propertyId);
        return response.data; // Assuming the API returns updated property data
    }
);

export const unpublishProperty = createAsyncThunk(
    "properties/unpublish",
    async (propertyId) => {
        const response = await propertyAPIService.unpublishProperty(propertyId);
        return response.data; // Assuming the API returns updated property data
    }
);

// Get all properties
export const getProperties = createAsyncThunk(
    "properties/getAll",
    async (_, thunkAPI) => {
        try {
            return await propertyAPIService.getProperties();
        } catch (error) {
            const message =
                (error.response &&
                    error.response.data &&
                    error.response.data.message) ||
                error.message ||
                error.toString();

            return thunkAPI.rejectWithValue(message);
        }
    }
);

const propertySlice = createSlice({
    name: "property",
    initialState,
    reducers: {
        reset: (state) => initialState,
    },

    extraReducers: (builder) => {
        builder
            .addCase(getProperties.pending, (state) => {
                state.isLoading = true;
            })
            .addCase(getProperties.fulfilled, (state, action) => {
                state.isLoading = false;
                state.isSuccess = true;
                state.properties = action.payload.results; // Assuming your API response has a "results" key
            })
            .addCase(getProperties.rejected, (state, action) => {
                state.loading = false;
                state.isError = true;
                state.message = action.payload;
            })
            .addCase(publishProperty.pending, (state) => {
                state.isLoading = true;
            })
            .addCase(publishProperty.fulfilled, (state) => {

                state.isLoading = false;
                state.isSuccess = true;
            })
            .addCase(publishProperty.rejected, (state, action) => {
                state.isLoading = false;
                state.error = action.error.message;
            })
            .addCase(unpublishProperty.pending, (state) => {
                state.isLoading = true;
            })
            .addCase(unpublishProperty.fulfilled, (state, action) => {


                state.isLoading = false;
                state.isSuccess = true;
            })

            .addCase(unpublishProperty.rejected, (state, action) => {
                state.isLoading = false;
                state.error = action.error.message;
            });
    },
});

export const { reset } = propertySlice.actions;
export default propertySlice.reducer;
