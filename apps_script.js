function condToSubject(condition) {
    var popularString = "Popular";
    var popularSubject = "Popular condition test"
    var personalString = "Personal";
    var personalSubject = "Personal condition test"
    if (condition == popularString) {
      return popularSubject;
    } else if (condition == personalString) {
      return personalSubject;
    } else {
      Logger.Log("Non-popular or personal condition detected");
    }
  }
  
  function condToMsg(condition) {
    var popularString = "Popular";
    var popularReminder = "Email body for popular condition";
    var personalString = "Personal";
    var personalReminder = "Email body for personal condition";
    if (condition == popularString) {
      return popularReminder;
    } else if (condition == personalString) {
      return personalReminder;
    } else {
      Logger.Log("Non-popular or personal condition detected");
    }
  }
  
  function triggerWrapper() {
    var sheet = SpreadsheetApp.openById('1aeJjpaWUwfPDasdGQjJZbLPVA8aVnxGEGBUyLK_Se1k');
    var responses = sheet.getSheetByName("responses");
  
    var range = responses.getRange("A2:H21");
    var vals = range.getValues();
    var sheetLength = vals.length;
  
    var allTriggers = ScriptApp.getProjectTriggers();
    var triggerCount = allTriggers.length;
  
    var address = vals[sheetLength - triggerCount][0]
    var subject = condToSubject(vals[sheetLength - triggerCount][1])
    var body = condToMsg(vals[sheetLength - triggerCount][1])
  
    GmailApp.sendEmail(address, subject, body);
  
    var triggerList = sheet.getSheetByName("triggers");
    var triggerVal = String(triggerList.getRange(sheetLength - triggerCount + 1, 1).getValue());
    for (var i = 0; i < triggerCount; i++) {
      Logger.log(allTriggers[i]);
      if (allTriggers[i].getUniqueId() === triggerVal) {
        ScriptApp.deleteTrigger(allTriggers[i]);
      }
    }
  }
  
  function createScheduleTrigger(triggerTime) {
    var sheet = SpreadsheetApp.openById('1aeJjpaWUwfPDasdGQjJZbLPVA8aVnxGEGBUyLK_Se1k');
    var triggerList = sheet.getSheetByName("triggers");
  
    var newTrigger = ScriptApp.newTrigger("triggerWrapper")
      .timeBased()
      .at(triggerTime)
      .create();
  
    triggerList.appendRow([newTrigger.getUniqueId()]);
  }
  
  function main() {
    var participantInfo = SpreadsheetApp.openById('1aeJjpaWUwfPDasdGQjJZbLPVA8aVnxGEGBUyLK_Se1k');
    var responses = participantInfo.getSheetByName("responses");
    var range = responses.getRange('A1:H21');
    var vals = range.getValues();
    for (var i = 1; i < vals.length; i++) {
      yr = vals[i][2];
      mth = vals[i][3];
      dy = vals[i][4];
      hr = vals[i][5];
      mn = vals[i][6];
      sec = vals[i][7];
      var time = new Date(yr, mth, dy, hr, mn, sec);
      createScheduleTrigger(time);
    }
  }