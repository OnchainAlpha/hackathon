# 🎨 Twenty CRM Frontend Integration Guide

## ✅ What We've Built

I've integrated an **AI-powered lead generation chat interface** directly into Twenty CRM's frontend! Here's what's been added:

### 📁 New Files Created

1. **`CRM/twenty/packages/twenty-front/src/modules/lead-gen/components/LeadGenChatModal.tsx`**
   - Beautiful modal with chat interface
   - Matches Twenty's design system
   - Real-time messaging
   - Example queries for quick start
   - Loading states and error handling

2. **`CRM/twenty/packages/twenty-front/src/modules/lead-gen/components/LeadGenChatButton.tsx`**
   - Floating action button (FAB)
   - Only appears on People page
   - Badge showing new contacts count
   - Smooth animations

3. **`CRM/twenty/packages/twenty-front/src/modules/lead-gen/index.ts`**
   - Module exports

### 📝 Modified Files

4. **`CRM/twenty/packages/twenty-front/src/modules/object-record/record-index/components/RecordIndexContainerGater.tsx`**
   - Added LeadGenChatButton import
   - Conditionally renders button only on People page
   - Passes recordTableId for table refresh

## 🎯 How It Works

### User Flow

```
1. User opens People page in Twenty CRM
   ↓
2. Sees floating blue robot button (bottom-right)
   ↓
3. Clicks button → Chat modal opens
   ↓
4. Types: "Find CTOs at AI companies in San Francisco"
   ↓
5. AI processes query → Scrapes contacts
   ↓
6. Contacts added to database
   ↓
7. Table automatically refreshes
   ↓
8. Badge shows number of new contacts
```

### Architecture

```
Frontend (React)                Backend (NestJS)              Python Service
     │                               │                              │
LeadGenChatModal ──POST──> /api/lead-gen/search ──HTTP──> FastAPI (port 8000)
     │                               │                              │
     │                          Parse query                   Apollo Scraper
     │                               │                              │
     │                          Create People                  Return contacts
     │                               │                              │
     └────────────────────────────── Response ─────────────────────┘
```

## 🚀 Next Steps

### Step 1: Build the Frontend

```bash
cd CRM/twenty/packages/twenty-front
yarn install
yarn build
```

### Step 2: Create Backend API Endpoint

You need to add a REST API endpoint to Twenty's NestJS server. Create this file:

**`CRM/twenty/packages/twenty-server/src/modules/lead-gen/lead-gen.controller.ts`**

```typescript
import { Controller, Post, Body } from '@nestjs/common';
import { LeadGenService } from './lead-gen.service';

@Controller('api/lead-gen')
export class LeadGenController {
  constructor(private readonly leadGenService: LeadGenService) {}

  @Post('search')
  async search(@Body() body: { query: string }) {
    return this.leadGenService.searchAndCreateContacts(body.query);
  }
}
```

**`CRM/twenty/packages/twenty-server/src/modules/lead-gen/lead-gen.service.ts`**

```typescript
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import axios from 'axios';

@Injectable()
export class LeadGenService {
  constructor(
    @InjectRepository(Person)
    private personRepository: Repository<Person>,
  ) {}

  async searchAndCreateContacts(query: string) {
    try {
      // Call your Python FastAPI service
      const response = await axios.post('http://localhost:8000/api/chat', {
        message: query,
      });

      const contacts = response.data.contacts || [];
      
      // Create people in Twenty CRM database
      const createdPeople = [];
      for (const contact of contacts) {
        const person = this.personRepository.create({
          name: {
            firstName: contact.name.split(' ')[0],
            lastName: contact.name.split(' ').slice(1).join(' '),
          },
          emails: {
            primaryEmail: contact.email,
          },
          phones: {
            primaryPhoneNumber: contact.phone,
          },
          jobTitle: contact.title,
          city: contact.city,
          linkedinLink: {
            primaryLinkUrl: contact.linkedin_url,
          },
        });
        
        const saved = await this.personRepository.save(person);
        createdPeople.push(saved);
      }

      return {
        message: `Found ${createdPeople.length} contacts and added them to your CRM!`,
        contactsAdded: createdPeople.length,
        contacts: createdPeople,
      };
    } catch (error) {
      console.error('Lead gen error:', error);
      throw new Error('Failed to search and create contacts');
    }
  }
}
```

**`CRM/twenty/packages/twenty-server/src/modules/lead-gen/lead-gen.module.ts`**

```typescript
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { LeadGenController } from './lead-gen.controller';
import { LeadGenService } from './lead-gen.service';
import { Person } from '../person/person.entity';

@Module({
  imports: [TypeOrmModule.forFeature([Person])],
  controllers: [LeadGenController],
  providers: [LeadGenService],
})
export class LeadGenModule {}
```

Then add to `app.module.ts`:

```typescript
import { LeadGenModule } from './modules/lead-gen/lead-gen.module';

@Module({
  imports: [
    // ... other modules
    LeadGenModule,
  ],
})
export class AppModule {}
```

### Step 3: Start Your Python Service

```bash
# Make sure your Python FastAPI service is running
python crm_integration/chat_api.py
```

### Step 4: Start Twenty CRM

```bash
cd CRM/twenty
yarn start
```

### Step 5: Test It!

1. Open Twenty CRM: http://localhost:3001
2. Navigate to People page
3. Click the blue robot button (bottom-right)
4. Type: "Find CTOs at AI companies in San Francisco"
5. Watch contacts appear in your CRM!

## 🎨 UI Features

### Floating Button
- **Position**: Fixed bottom-right
- **Color**: Blue (matches Twenty's primary color)
- **Icon**: Robot icon
- **Badge**: Shows count of new contacts
- **Animation**: Hover scale, smooth transitions

### Chat Modal
- **Size**: 500px × 600px
- **Header**: Title with robot icon, close button
- **Messages**: User messages (blue), AI responses (gray)
- **Input**: Multi-line textarea with send button
- **Examples**: Quick-start example queries
- **Empty State**: Friendly message with examples

### Design System
- Uses Twenty's theme system
- Matches Twenty's spacing, colors, typography
- Responsive and accessible
- Smooth animations

## 🔧 Customization

### Change Button Position

Edit `LeadGenChatButton.tsx`:

```typescript
const StyledFloatingButton = styled.button`
  bottom: ${({ theme }) => theme.spacing(6)}; // Change this
  right: ${({ theme }) => theme.spacing(6)};  // Change this
`;
```

### Change Button Color

```typescript
background: ${({ theme }) => theme.color.blue}; // Change to theme.color.green, etc.
```

### Add More Example Queries

Edit `LeadGenChatModal.tsx`:

```typescript
const EXAMPLE_QUERIES = [
  'Find CTOs at AI companies in San Francisco',
  'Get investors in the FinTech space',
  'Your custom query here',
];
```

### Show Button on Other Pages

Edit `RecordIndexContainerGater.tsx`:

```typescript
// Show on Companies page too
const showLeadGenButton = 
  objectMetadataItem.namePlural === 'people' || 
  objectMetadataItem.namePlural === 'companies';
```

## 📊 Data Flow

### Frontend → Backend

```json
POST /api/lead-gen/search
{
  "query": "Find CTOs at AI companies in San Francisco"
}
```

### Backend → Python Service

```json
POST http://localhost:8000/api/chat
{
  "message": "Find CTOs at AI companies in San Francisco"
}
```

### Python Service → Backend

```json
{
  "response": "Found 23 contacts!",
  "contacts_found": 23,
  "contacts": [
    {
      "name": "John Smith",
      "email": "john@example.com",
      "title": "CTO",
      "company": "AI Startup",
      "city": "San Francisco",
      "linkedin_url": "https://linkedin.com/in/johnsmith"
    }
  ]
}
```

### Backend → Frontend

```json
{
  "message": "Found 23 contacts and added them to your CRM!",
  "contactsAdded": 23,
  "contacts": [...]
}
```

## 🐛 Troubleshooting

### Button Not Showing
- Check if you're on the People page
- Check browser console for errors
- Verify the module is imported correctly

### Modal Not Opening
- Check browser console for errors
- Verify Modal component is imported
- Check if isOpen state is working

### API Errors
- Verify Python service is running on port 8000
- Check NestJS server logs
- Verify CORS is configured correctly
- Check network tab in browser dev tools

### Contacts Not Appearing
- Check if contacts are being created in database
- Verify table refresh is working
- Check Person entity schema matches

### Build Errors
- Run `yarn install` in twenty-front
- Clear node_modules and reinstall
- Check TypeScript errors

## 🎉 Features

✅ **AI-Powered** - Natural language queries
✅ **Beautiful UI** - Matches Twenty's design system
✅ **Real-Time** - Instant feedback and updates
✅ **Smart** - Only shows on People page
✅ **Integrated** - Uses Twenty's components and hooks
✅ **Responsive** - Works on all screen sizes
✅ **Accessible** - Keyboard navigation, ARIA labels
✅ **Animated** - Smooth transitions and effects

## 📚 Resources

- **Twenty CRM Docs**: https://docs.twenty.com
- **Twenty UI Components**: `CRM/twenty/packages/twenty-ui`
- **Apollo Scraper**: `scrapers/apollo_scraper.py`
- **Python API**: `crm_integration/chat_api.py`

## 🚀 Production Deployment

### Environment Variables

```bash
# .env
PYTHON_API_URL=https://your-python-api.com
OPENAI_API_KEY=sk-your-key
APOLLO_API_KEY=your-apollo-key
```

### Update API URL

In `lead-gen.service.ts`:

```typescript
const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:8000';
```

### Build for Production

```bash
cd CRM/twenty
yarn build
yarn start:prod
```

## 🎊 You're All Set!

Your Twenty CRM now has an integrated AI lead generation system! Users can:
1. Click the robot button
2. Describe what they want
3. Get contacts automatically added to their CRM

**It's that simple!** 🚀

---

Built with ❤️ for the LeadOn CRM Hackathon

