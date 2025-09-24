# 🏃‍♂️☕ Saturday Run & Coffee Club

> *A mindful Saturday morning ritual combining 5km running, specialty coffee, and productive activities. Join us at 8 AM for an energizing start to your weekend, connecting with like-minded individuals who value wellness, growth, and meaningful conversations.*

## ✨ Features

- **📅 Automatic Event Scheduling**: Shows next Saturday's event automatically
- **👥 Easy Registration**: Simple web form for participants to join
- **📊 Live Participant Count**: Real-time display of who's coming
- **📱 Mobile Responsive**: Beautiful design inspired by Aman Hotels & Wellness Retreats
- **🔄 GitHub Integration**: Uses GitHub Issues API for event management (optional)

## 🚀 Quick Setup & Deployment

### Option 1: GitHub Pages (Recommended - Free & Easy)

1. **Fork or Create Repository**
   ```bash
   # Create new repository on GitHub named 'saturday-run-coffee-club'
   # Upload all files from this directory
   ```

2. **Enable GitHub Pages**
   - Go to repository Settings
   - Scroll to "Pages" section
   - Source: Deploy from a branch
   - Branch: main / (root)
   - Save

3. **Your site will be live at:**
   ```
   https://YOUR_USERNAME.github.io/saturday-run-coffee-club
   ```

### Option 2: Advanced GitHub Integration

For full GitHub API integration (participant management via Issues):

1. **Configure GitHub API**
   - Edit `js/app.js`
   - Replace `YOUR_GITHUB_USERNAME` with your actual username
   - Create a GitHub Personal Access Token (Settings → Developer settings → Personal access tokens)

2. **Create Event Issues**
   - Create GitHub Issues with label "event" for each Saturday
   - Participants will be added as comments automatically

3. **Environment Setup** (for production)
   ```bash
   # Set environment variable for GitHub token
   export GITHUB_TOKEN=your_personal_access_token
   ```

## 📁 Project Structure

```
saturday-run-coffee-club/
├── index.html          # Main page
├── css/
│   └── style.css      # Aman/Wellness inspired styling
├── js/
│   └── app.js         # GitHub API integration & functionality
├── images/            # Image assets (add your photos here)
├── docs/              # Additional documentation
└── README.md          # This file
```

## 🎨 Design Philosophy

Inspired by **Aman Hotels & Resorts** and **Wellness Retreats**:

- **Minimalist Elegance**: Clean lines, generous whitespace
- **Natural Color Palette**: Warm beiges, soft sage, charcoal
- **Premium Typography**: Inter font family for modern readability
- **Mindful Interactions**: Subtle animations, thoughtful user experience
- **Mobile-First**: Responsive design for all devices

## 🔧 Customization

### Colors & Branding
Edit CSS variables in `css/style.css`:
```css
:root {
    --primary-beige: #F5F1E8;
    --warm-white: #FEFCF7;
    --soft-sage: #E8F0E8;
    --charcoal: #2C2C2C;
    --accent-gold: #D4AF37;
}
```

### Content Updates
- **Club Description**: Edit hero section in `index.html`
- **Meeting Details**: Update time/location in JavaScript
- **About Section**: Customize values and messaging

### Adding Images
1. Add images to `images/` folder
2. Update CSS background images or HTML img tags
3. Recommended: High-quality photos of running, coffee, nature

## 📱 Usage Guide

### For Club Organizers
1. **Weekly Setup**: Create new GitHub Issue with "event" label (if using GitHub integration)
2. **Announcements**: Update event details in the Issue description
3. **Participant Management**: View registrations as Issue comments

### For Participants
1. **Visit Website**: Go to your club's URL
2. **View Next Event**: Automatically shows next Saturday
3. **Register**: Fill out simple form with name and contact
4. **Confirmation**: Receive success message after registration

## 🛠️ Technical Details

### Dependencies
- **No Build Process**: Pure HTML/CSS/JavaScript
- **No Database**: Uses GitHub API or localStorage
- **No Server**: Static site hosting
- **Fonts**: Google Fonts (Inter)

### Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Progressive enhancement for older browsers

### Performance
- Lightweight: < 50KB total size
- Fast loading: Optimized CSS and JavaScript
- CDN fonts: Google Fonts with preconnect

## 🔒 Privacy & Security

- **No Personal Data Storage**: Only names and contact info
- **GitHub Integration**: Uses public repositories (consider privacy)
- **Local Fallback**: Works without GitHub API
- **No Tracking**: No analytics or third-party scripts

## 🆘 Troubleshooting

### Common Issues

**"Loading next event..." doesn't update**
- Check GitHub API configuration in `js/app.js`
- Verify repository name and username
- Ensure GitHub Pages is enabled

**Form submission fails**
- Works locally with localStorage fallback
- For GitHub integration, check Personal Access Token
- Verify repository permissions

**Styling looks broken**
- Check CSS file path in `index.html`
- Ensure all files are uploaded to correct directories
- Clear browser cache

### Support

For technical issues or customization help:
1. Check browser console for error messages
2. Verify all files are properly uploaded
3. Test locally first, then deploy

## 📄 License

This project is open source and available under the MIT License.

---

*Crafted with intention for mindful Saturday mornings. 🌅*
