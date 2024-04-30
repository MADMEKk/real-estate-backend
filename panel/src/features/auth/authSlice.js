import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import authService from "./authAPIServices";

const user = JSON.parse(localStorage.getItem("user"));


// Thunk action to refresh the token
export const refreshAccessToken = createAsyncThunk("auth/refreshAccessToken", async (_, thunkAPI) => {
  try {
    return await authService.refresh();
  } catch (error) {
    return thunkAPI.rejectWithValue(error.message);
  }
});

// Thunk action to verify the token
export const verifyToken = createAsyncThunk("auth/verifyToken", async (_, thunkAPI) => {
  try {
    return await authService.verifyToken();
  } catch (error) {
    return thunkAPI.rejectWithValue(error.message);
  }
});

const initialState = {
  user: user ? user : null,
  isError: false,
  isLoading: false,
  isSuccess: false,
  message: "",
};
export const register = createAsyncThunk(
  "auth/register",
  async (user, thunkAPI) => {
    try {
      return await authService.register(user);
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
export const login = createAsyncThunk("auth/login", async (user, thunkAPI) => {
  try {
    return await authService.login(user);
  } catch (error) {
    const message =
      (error.response && error.response.data && error.response.data.message) ||
      error.message ||
      error.toString();

    return thunkAPI.rejectWithValue(message);
  }
});

export const logout = createAsyncThunk("auth/logout", async () => {
  authService.logout();
});
export const activate = createAsyncThunk(
  "auth/activate",
  async (user, thunkAPI) => {
    try {
      return await authService.activate(user);
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

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    reset: (state) => {
      state.isError = false;
      state.isLoading = false;
      state.isSuccess = false;
      state.message = "";
    },
  },
  extraReducers: (builder) => {
    builder
        .addCase(refreshAccessToken.fulfilled, (state, action) => {
          state.isLoading = false;
          if (action.payload.access) {
            state.user.access = action.payload.access;
          } else {
            state.isError = true;
            state.message = "Token refresh failed";
          }
        })
        .addCase(refreshAccessToken.rejected, (state, action) => {
          state.isLoading = false;
          state.isError = true;
          state.message = action.payload;
          state.user = null;
        })
        .addCase(verifyToken.fulfilled, (state, action) => {
          state.isLoading = false;
          if (!action.payload.code) {
            // Token is valid
            state.user = action.payload;
          } else {
            // Token is invalid
            state.isError = true;
            state.message = "Token verification failed";
            state.user = null;
          }
        })
        .addCase(verifyToken.rejected, (state, action) => {
          state.isLoading = false;
          state.isError = true;
          state.message = action.payload;
          state.user = null;
        })
      .addCase(register.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(register.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSuccess = true;
      })
      .addCase(register.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
        state.user = null;
      })
      .addCase(login.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSuccess = true;
        state.user = action.payload;
      })
      .addCase(login.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
        state.user = null;
      })
      .addCase(logout.fulfilled, (state) => {
        state.user = null;
      })
      .addCase(activate.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(activate.fulfilled, (state) => {
        state.isLoading = false;
        state.isSuccess = true;
      })
      .addCase(activate.rejected, (state, action) => {
        state.isLoading = false;
        state.isError = true;
        state.message = action.payload;
        state.user = null;
      });
  },
});

export const { reset } = authSlice.actions;
export default authSlice.reducer;
