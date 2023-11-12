<h1>flight_mails</h1>
<p>The program takes user name and email as an input. It stores users info in a googlesheet. The flight requirements like desired destination and prizes are stored in another google sheet. It reads and writes google sheets using Google APIs and gspread module. The data of desired destinations are collected from an API to find cheapest routes. The data is converted into a message containing total cost, duration and flight exchanges. The message is e-mailed to all users in the spread sheet.</p>
<h3>This project is built in Python 3 using:</h3>
<ol>
  <li>Modules: Requests, Smtplib and Gspread</li>
  <li>APIs: Tequila and Google APIs</li>
</ol>
