# 🔐 Admin Dashboard Credentials

## Superuser Account

**Username:** `peterstoyanov`  
**Password:** `CoachingMaster2024!`

## Access URLs

- **Admin Dashboard:** `http://localhost:8000/admin/dashboard`
- **Statistics API:** `http://localhost:8000/admin/stats`
- **Recent Activity:** `http://localhost:8000/admin/recent-activity`
- **Email Export:** `http://localhost:8000/admin/emails`

## Security Features

✅ **JWT Authentication** - Secure token-based authentication  
✅ **Password Hashing** - Bcrypt encryption for password security  
✅ **Session Management** - Auto-logout on token expiration  
✅ **Protected Routes** - All admin endpoints require authentication  
✅ **Strong Password** - Complex password with special characters  

## Login Process

1. Go to `http://localhost:8000/admin/dashboard`
2. Enter credentials:
   - Username: `peterstoyanov`
   - Password: `CoachingMaster2024!`
3. Dashboard loads automatically
4. Session persists in browser localStorage
5. Auto-refreshes data every 30 seconds

## API Authentication

For programmatic access to admin APIs:

```bash
# 1. Get access token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=peterstoyanov&password=CoachingMaster2024!"

# 2. Use token in subsequent requests
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  "http://localhost:8000/admin/stats"
```

## Security Notes

⚠️ **Important for Production:**
1. Change the SECRET_KEY in environment variables
2. Use HTTPS for all admin access
3. Consider IP whitelisting for admin routes
4. Store credentials securely (not in plain text)
5. Implement password rotation policy

## Token Expiration

- **Access tokens expire after 60 minutes**
- **Automatic logout** when token expires
- **Re-login required** for continued access

## Password Policy

Current password meets security requirements:
- ✅ 16+ characters
- ✅ Uppercase and lowercase letters
- ✅ Numbers and special characters
- ✅ No common dictionary words

---

**Keep these credentials secure and do not share them!** 🔒