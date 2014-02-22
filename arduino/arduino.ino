/*
   Web client sketch for IDE v1.0.1 and w5100/w5200
   Uses POST method.
   Posted November 2012 by SurferTim
 */

#include <LiquidCrystal.h>
#include <SPI.h>
#include <Ethernet.h>


// Scanner
// ==========
int SCAN_ENTER = 0x5a; int SCAN_BREAK = 0xf0;
int breakActive = 0;
int clockPin = A2; // Clock is only output.
int dataPin = A1; // The data pin is bi-directional

int clockValue = 0;
byte dataValue;
byte scanCodes[10] = {0x45,0x16,0x1e,0x26,0x25,0x2e,0x36,0x3d,0x3e,0x46};
char characters[10] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};
int quantityCodes = 10;
char buffer[64] = {};   // This saves the characters (for now only numbers)
int bufferPos = 0;
int bufferLength = 64;

// Ethernet
// ===========
byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

//Change to your server domain
char serverName[] = "3d082f.ngrok.com";

// change to your server's port
int serverPort = 80;

EthernetClient client;
int totalCount = 0;
// insure params is big enough to hold your variables
char params[64];

// LCD
// ======
// select the pins used on the LCD panel
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

// define some values used by the panel and buttons
int lcd_key     = 0;
int adc_key_in  = 0;
#define btnRIGHT  0
#define btnUP     1
#define btnDOWN   2
#define btnLEFT   3
#define btnSELECT 4
#define btnNONE   5

void setup() {

  // initialize pins for barcode scanner
  pinMode(dataPin, INPUT);
  pinMode(clockPin, INPUT);

  // start lcd library
  lcd.begin(16, 2);
  lcd.setCursor(0,0);

  Serial.begin(9600);

  // start the Ethernet connection:
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // no point in carrying on, so do nothing forevermore:
    for(;;)
      ;
  }
  // print your local IP address:
  Serial.print("My IP address: ");
  for (byte thisByte = 0; thisByte < 4; thisByte++) {
    // print the value of each byte of the IP address:
    Serial.print(Ethernet.localIP()[thisByte], DEC);
    Serial.print(".");
  }

   delay(2000);
   Serial.println(F("Ready"));
   lcd.print(F("Gatavs vergot"));
}

void loop()
{

  dataValue = dataRead();

  // If there is a break code, skip the next byte
  if (dataValue == SCAN_BREAK) {
    breakActive = 1;
  }

  // Translate the scan codes to numbers
  // If there is a match, store it to the buffer
  for (int i = 0; i < quantityCodes; i++) {
    byte temp = scanCodes[i];
    if(temp == dataValue){
      if(!breakActive == 1){
        buffer[bufferPos] = characters[i];
        bufferPos++;
      }
    }
  }

  // Print the buffer if SCAN_ENTER is pressed.
  if(dataValue == SCAN_ENTER){

    lcd.clear();
    lcd.print(buffer);
    lcd.setCursor(0,1);
    lcd.print("MEKLEJU...");

    lookupProduct(buffer);

    removeProduct(buffer);

    Serial.println(buffer);

    bufferPos = 0;

  }
  // Reset the SCAN_BREAK state if the byte was a normal one
  if(dataValue != SCAN_BREAK){

    breakActive = 0;
  }
  dataValue = 0;
}

byte postPage(char* domainBuffer,int thisPort,char* page,char* thisData) {
  int inChar;
  char outBuf[64];

  Serial.print(F("connecting..."));

  if(client.connect(domainBuffer,thisPort))
  {
    Serial.println(F("connected"));

    // send the header
    sprintf(outBuf,"POST %s HTTP/1.1",page);
    client.println(outBuf);
    sprintf(outBuf,"Host: %s",domainBuffer);
    client.println(outBuf);
    client.println(F("Connection: close\r\nContent-Type: application/x-www-form-urlencoded"));
    sprintf(outBuf,"Content-Length: %u\r\n",strlen(thisData));
    client.println(outBuf);

    // send the body (variables)
    client.print(thisData);

    String response;
    char c;

    // Get the response
    while(client.connected() && !client.available()) delay(1);
      while (client.available()) {
        c = client.read();
        response = response + c;
      }

    // Get response body
    // Headers end with double CRLF
    int contentBodyIndex = response.lastIndexOf('\n\r\n\r');
    if (contentBodyIndex > 0) {
        lcd.clear();
        // Offset  for 2 linefeeds
        lcd.print(response.substring(contentBodyIndex+2));
    }

  }
  else
  {
    Serial.println(F("POST failed"));
    return 0;
  }

  int connectLoop = 0;

  while(client.connected())
  {
    while(client.available())
    {
      inChar = client.read();
      Serial.write(inChar);
      connectLoop = 0;
    }

    delay(1);
    connectLoop++;
    if(connectLoop > 10)
    {
      Serial.println();
      Serial.println(F("Timeout"));
      client.stop();
    }
  }

  Serial.println();
  Serial.println(F("disconnecting."));
  client.stop();
  client.flush();
  return 1;
}

byte getPage(char* domainBuffer,int thisPort,char* page) {
  int inChar;
  char outBuf[64];

  Serial.print(F("connecting..."));

  if(client.connect(domainBuffer,thisPort))
  {
    Serial.println(F("connected"));

    // send the header
    sprintf(outBuf,"GET %s HTTP/1.1",page);
    client.println(outBuf);
    sprintf(outBuf,"Host: %s",domainBuffer);
    client.println(outBuf);
    client.println(F("Connection: close\r\nContent-Type: application/x-www-form-urlencoded"));
    client.println("");

    String response;
    char c;

    // Get the response
    while(client.connected() && !client.available()) delay(1);
      while (client.available()) {
        c = client.read();
        response = response + c;
      }

    // Get response body
    // Headers end with double CRLF
    int contentBodyIndex = response.lastIndexOf('\n\r\n\r');
    if (contentBodyIndex > 0) {
        lcd.clear();
        // Offset  for 2 linefeeds
        lcd.print(response.substring(contentBodyIndex+2));
    }

  }
  else
  {
    Serial.println(F("POST failed"));
    return 0;
  }

  int connectLoop = 0;

  while(client.connected())
  {
    while(client.available())
    {
      inChar = client.read();
      Serial.write(inChar);
      connectLoop = 0;
    }

    delay(1);
    connectLoop++;
    if(connectLoop > 10)
    {
      Serial.println();
      Serial.println(F("Timeout"));
      client.stop();
    }
  }

  Serial.println();
  Serial.println(F("disconnecting."));
  client.stop();
  client.flush();
  return 1;
}

int dataRead() {
    byte val = 0;
    // Skip start state and start bit
    while (digitalRead(clockPin));  // Wait for LOW.
    // clock is high when idle
    while (!digitalRead(clockPin)); // Wait for HIGH.
    while (digitalRead(clockPin));  // Wait for LOW.
    for (int offset = 0; offset < 8; offset++) {
        while (digitalRead(clockPin));         // Wait for LOW
        val |= digitalRead(dataPin) << offset; // Add to byte
        while (!digitalRead(clockPin));        // Wait for HIGH
    }
    // Skipping parity and stop bits down here.
    while (digitalRead(clockPin));           // Wait for LOW.
    while (!digitalRead(clockPin));          // Wait for HIGH.
    while (digitalRead(clockPin));           // Wait for LOW.
    while (!digitalRead(clockPin));          // Wait for HIGH.
    return val;
}

void lookupProduct(char* ean) {
    // params must be url encoded.
    char pageName[64];
    sprintf(pageName,"/prece/atrast?ean=%s", ean);
    if(!getPage(serverName,serverPort,pageName)) {
        Serial.print(F("Fail "));
        lcd.clear();
        lcd.print(F("Blje sapliisa"));
    }
    else {
        Serial.print(F("Pass "));
    }
}

void removeProduct(char* ean) {
    // params must be url encoded.
    char pageName[] = "/prece/nonemt";
    sprintf(params,"ean=%s&quantity=%s&eka=%s", ean, "1", "1360");
    if(!postPage(serverName,serverPort,pageName,params)) {
        Serial.print(F("Fail "));
        lcd.clear();
        lcd.print(F("Blje sapliisa"));
    }
    else {
        Serial.print(F("Pass "));
    }
}



