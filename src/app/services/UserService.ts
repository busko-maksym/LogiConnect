import axios from 'axios';

export const fetchUserData = async (userId: string) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/user/${userId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching user data:', error);
    return null;
  }
};
