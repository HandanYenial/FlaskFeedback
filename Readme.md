# Flask Feedback

**Introduction:**
Flask FeedBack is a web application that allows users to sign up and log in to their individual accounts. Once logged in, users can provide feedback, edit their feedback, delete their feedback, and view a list of all the feedback they have submitted. Routes are protected to prevent unauthorized access. For instance, user1 cannot edit feedback created by user2.

**Features:**
1. **User Authentication:**
   - Users can sign up and create their accounts.
   - Existing users can log in with their credentials.

2. **Feedback Management:**
   - Logged-in users can submit feedback.
   - Users can edit or update their own feedback.
   - Feedback can be deleted by the user who submitted it.

3. **Feedback List:**
    - Users can view a list of all feedback they have provided.

4. **Access Control:**
    - Routes and actions are protected to ensure data privacy.
    - Users can only edit and delete the feedback they have submitted, not others'.
      
**Routes**

**/register**: Allows users to create a new account by providing a username, password, email, first name, and last name.

**/login**: Allows users to log in to their account with an email and password.

**/users/username**: Shows information about the logged-in user.

**/users/username/delete**: Removes the user from the database and delete all of their feedback.

**Conclusion:**
Flask FeedBack simplifies feedback management by providing a user-friendly interface for submitting, editing, and viewing feedback. With proper access control, users can feel confident that their feedback remains private and secure. 
