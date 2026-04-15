#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8531.81852a8bc modeling language!
# line 5 "../../driver_license_system.ump"
import os
from enum import Enum, auto

class Applicant():
    applicantsByApplicantId = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Applicant Attributes
    #Applicant State Machines
    class LicenseLifecycle(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        NoLicense = auto()
        Licensed = auto()
        Suspended = auto()
        ExpiredG = auto()

    class LicenseLifecycleLicensed(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        Null = auto()
        G1 = auto()
        G2 = auto()
        G = auto()

    #Applicant Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aApplicantId):
        self._testRecords = None
        self._currentLicense = None
        self._licenseLifecycleLicensed = None
        self._licenseLifecycle = None
        self._suspensionCode = None
        self._lastScore = None
        self._feePaid = None
        self._addressCode = None
        self._birthYear = None
        self._nameCode = None
        self._applicantId = None
        self._nameCode = 101
        self._birthYear = 1990
        self._addressCode = 501
        self._feePaid = 0
        self._lastScore = 0
        self._suspensionCode = 0
        if not self.setApplicantId(aApplicantId) :
            raise RuntimeError ("Cannot create due to duplicate applicantId. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        self._testRecords = []
        self.setLicenseLifecycleLicensed(Applicant.LicenseLifecycleLicensed.Null)
        self.setLicenseLifecycle(Applicant.LicenseLifecycle.NoLicense)

    #------------------------
    # INTERFACE
    #------------------------
    def setApplicantId(self, aApplicantId):
        wasSet = False
        anOldApplicantId = self.getApplicantId()
        if not (anOldApplicantId is None) and anOldApplicantId == aApplicantId :
            return True
        if Applicant.hasWithApplicantId(aApplicantId) :
            return wasSet
        self._applicantId = aApplicantId
        wasSet = True
        if not (anOldApplicantId is None) :
            Applicant.applicantsByApplicantId.pop(anOldApplicantId, None)
        Applicant.applicantsByApplicantId[aApplicantId] = self
        return wasSet

    def setNameCode(self, aNameCode):
        wasSet = False
        self._nameCode = aNameCode
        wasSet = True
        return wasSet

    def setBirthYear(self, aBirthYear):
        wasSet = False
        self._birthYear = aBirthYear
        wasSet = True
        return wasSet

    def setAddressCode(self, aAddressCode):
        wasSet = False
        self._addressCode = aAddressCode
        wasSet = True
        return wasSet

    def setFeePaid(self, aFeePaid):
        wasSet = False
        self._feePaid = aFeePaid
        wasSet = True
        return wasSet

    def setLastScore(self, aLastScore):
        wasSet = False
        self._lastScore = aLastScore
        wasSet = True
        return wasSet

    def setSuspensionCode(self, aSuspensionCode):
        wasSet = False
        self._suspensionCode = aSuspensionCode
        wasSet = True
        return wasSet

    def getApplicantId(self):
        return self._applicantId

    # Code from template attribute_GetUnique 
    @staticmethod
    def getWithApplicantId(aApplicantId):
        return Applicant.applicantsByApplicantId.get(aApplicantId)

    # Code from template attribute_HasUnique 
    @staticmethod
    def hasWithApplicantId(aApplicantId):
        return not (Applicant.getWithApplicantId(aApplicantId) is None)

    def getNameCode(self):
        return self._nameCode

    def getBirthYear(self):
        return self._birthYear

    def getAddressCode(self):
        return self._addressCode

    def getFeePaid(self):
        return self._feePaid

    def getLastScore(self):
        return self._lastScore

    def getSuspensionCode(self):
        return self._suspensionCode

    def getLicenseLifecycleFullName(self):
        answer = self._licenseLifecycle.__str__()
        if self._licenseLifecycleLicensed != Applicant.LicenseLifecycleLicensed.Null :
            answer += "." + self._licenseLifecycleLicensed.__str__()
        return answer

    def getLicenseLifecycle(self):
        return self._licenseLifecycle

    def getLicenseLifecycleLicensed(self):
        return self._licenseLifecycleLicensed

    def payFee(self):
        wasEventProcessed = False
        aLicenseLifecycle = self._licenseLifecycle
        aLicenseLifecycleLicensed = self._licenseLifecycleLicensed
        if aLicenseLifecycle == Applicant.LicenseLifecycle.NoLicense :
            # line 32 "../../driver_license_system.ump"
            self.setFeePaid(1)
            self.setLicenseLifecycle(Applicant.LicenseLifecycle.NoLicense)
            wasEventProcessed = True
        else :
            # Other states do respond to this event
            pass
        if aLicenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G1 :
            self.exitLicenseLifecycleLicensed()
            # line 42 "../../driver_license_system.ump"
            self.setFeePaid(1)
            self.setLicenseLifecycleLicensed(Applicant.LicenseLifecycleLicensed.G1)
            wasEventProcessed = True
        elif aLicenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G2 :
            self.exitLicenseLifecycleLicensed()
            # line 53 "../../driver_license_system.ump"
            self.setFeePaid(1)
            self.setLicenseLifecycleLicensed(Applicant.LicenseLifecycleLicensed.G2)
            wasEventProcessed = True
        else :
            # Other states do respond to this event
            pass
        return wasEventProcessed

    def passG1Test(self):
        wasEventProcessed = False
        aLicenseLifecycle = self._licenseLifecycle
        if aLicenseLifecycle == Applicant.LicenseLifecycle.NoLicense :
            if self.getFeePaid() == 1 :
                # line 33 "../../driver_license_system.ump"
                self.setLastScore(80)
                self.setFeePaid(0)
                self.setLicenseLifecycleLicensed(Applicant.LicenseLifecycleLicensed.G1)
                wasEventProcessed = True
        else :
            # Other states do respond to this event
            pass
        return wasEventProcessed

    def reinstateAsG1(self):
        wasEventProcessed = False
        aLicenseLifecycle = self._licenseLifecycle
        if aLicenseLifecycle == Applicant.LicenseLifecycle.Suspended :
            if self.getSuspensionCode() == 1 :
                # line 70 "../../driver_license_system.ump"
                self.setSuspensionCode(0)
                self.setLicenseLifecycleLicensed(Applicant.LicenseLifecycleLicensed.G1)
                wasEventProcessed = True
        else :
            # Other states do respond to this event
            pass
        return wasEventProcessed

    def reinstateAsG2(self):
        wasEventProcessed = False
        aLicenseLifecycle = self._licenseLifecycle
        if aLicenseLifecycle == Applicant.LicenseLifecycle.Suspended :
            if self.getSuspensionCode() == 2 :
                # line 71 "../../driver_license_system.ump"
                self.setSuspensionCode(0)
                self.setLicenseLifecycleLicensed(Applicant.LicenseLifecycleLicensed.G2)
                wasEventProcessed = True
        else :
            # Other states do respond to this event
            pass
        return wasEventProcessed

    def reinstateAsG(self):
        wasEventProcessed = False
        aLicenseLifecycle = self._licenseLifecycle
        if aLicenseLifecycle == Applicant.LicenseLifecycle.Suspended :
            if self.getSuspensionCode() == 3 :
                # line 72 "../../driver_license_system.ump"
                self.setSuspensionCode(0)
                self.setLicenseLifecycleLicensed(Applicant.LicenseLifecycleLicensed.G)
                wasEventProcessed = True
        else :
            # Other states do respond to this event
            pass
        return wasEventProcessed

    def renewG(self):
        wasEventProcessed = False
        aLicenseLifecycle = self._licenseLifecycle
        if aLicenseLifecycle == Applicant.LicenseLifecycle.ExpiredG :
            self.setLicenseLifecycleLicensed(Applicant.LicenseLifecycleLicensed.G)
            wasEventProcessed = True
        else :
            # Other states do respond to this event
            pass
        return wasEventProcessed

    def passG2Test(self):
        wasEventProcessed = False
        aLicenseLifecycleLicensed = self._licenseLifecycleLicensed
        if aLicenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G1 :
            if self.getFeePaid() == 1 :
                self.exitLicenseLifecycleLicensed()
                # line 43 "../../driver_license_system.ump"
                self.setLastScore(82)
                self.setFeePaid(0)
                self.setLicenseLifecycleLicensed(Applicant.LicenseLifecycleLicensed.G2)
                wasEventProcessed = True
        else :
            # Other states do respond to this event
            pass
        return wasEventProcessed

    def expire(self):
        wasEventProcessed = False
        aLicenseLifecycleLicensed = self._licenseLifecycleLicensed
        if aLicenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G1 :
            self.exitLicenseLifecycle()
            self.setLicenseLifecycle(Applicant.LicenseLifecycle.NoLicense)
            wasEventProcessed = True
        elif aLicenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G2 :
            self.exitLicenseLifecycle()
            self.setLicenseLifecycle(Applicant.LicenseLifecycle.NoLicense)
            wasEventProcessed = True
        elif aLicenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G :
            self.exitLicenseLifecycle()
            self.setLicenseLifecycle(Applicant.LicenseLifecycle.ExpiredG)
            wasEventProcessed = True
        else :
            # Other states do respond to this event
            pass
        return wasEventProcessed

    def suspend(self):
        wasEventProcessed = False
        aLicenseLifecycleLicensed = self._licenseLifecycleLicensed
        if aLicenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G1 :
            self.exitLicenseLifecycle()
            # line 48 "../../driver_license_system.ump"
            self.setSuspensionCode(1)
            self.setLicenseLifecycle(Applicant.LicenseLifecycle.Suspended)
            wasEventProcessed = True
        elif aLicenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G2 :
            self.exitLicenseLifecycle()
            # line 59 "../../driver_license_system.ump"
            self.setSuspensionCode(2)
            self.setLicenseLifecycle(Applicant.LicenseLifecycle.Suspended)
            wasEventProcessed = True
        elif aLicenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G :
            self.exitLicenseLifecycle()
            # line 65 "../../driver_license_system.ump"
            self.setSuspensionCode(3)
            self.setLicenseLifecycle(Applicant.LicenseLifecycle.Suspended)
            wasEventProcessed = True
        else :
            # Other states do respond to this event
            pass
        return wasEventProcessed

    def passGTest(self):
        wasEventProcessed = False
        aLicenseLifecycleLicensed = self._licenseLifecycleLicensed
        if aLicenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G2 :
            if self.getFeePaid() == 1 :
                self.exitLicenseLifecycleLicensed()
                # line 54 "../../driver_license_system.ump"
                self.setLastScore(88)
                self.setFeePaid(0)
                self.setLicenseLifecycleLicensed(Applicant.LicenseLifecycleLicensed.G)
                wasEventProcessed = True
        else :
            # Other states do respond to this event
            pass
        return wasEventProcessed

    def exitLicenseLifecycle(self):
        if self._licenseLifecycle == Applicant.LicenseLifecycle.Licensed :
            self.exitLicenseLifecycleLicensed()

    def setLicenseLifecycle(self, aLicenseLifecycle):
        self._licenseLifecycle = aLicenseLifecycle
        # entry actions and do activities
        if self._licenseLifecycle == Applicant.LicenseLifecycle.Licensed :
            if self._licenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.Null :
                self.setLicenseLifecycleLicensed(Applicant.LicenseLifecycleLicensed.G1)

    def exitLicenseLifecycleLicensed(self):
        if self._licenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G1 :
            self.setLicenseLifecycleLicensed(Applicant.LicenseLifecycleLicensed.Null)
        elif self._licenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G2 :
            self.setLicenseLifecycleLicensed(Applicant.LicenseLifecycleLicensed.Null)
        elif self._licenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G :
            self.setLicenseLifecycleLicensed(Applicant.LicenseLifecycleLicensed.Null)

    def setLicenseLifecycleLicensed(self, aLicenseLifecycleLicensed):
        self._licenseLifecycleLicensed = aLicenseLifecycleLicensed
        if self._licenseLifecycle != Applicant.LicenseLifecycle.Licensed and aLicenseLifecycleLicensed != Applicant.LicenseLifecycleLicensed.Null :
            self.setLicenseLifecycle(Applicant.LicenseLifecycle.Licensed)
        # entry actions and do activities
        if self._licenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G1 :
            # line 41 "../../driver_license_system.ump"
            self.setSuspensionCode(0)
        elif self._licenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G2 :
            # line 52 "../../driver_license_system.ump"
            self.setSuspensionCode(0)
        elif self._licenseLifecycleLicensed == Applicant.LicenseLifecycleLicensed.G :
            # line 63 "../../driver_license_system.ump"
            self.setSuspensionCode(0)

    # Code from template association_GetOne 
    def getCurrentLicense(self):
        return self._currentLicense

    def hasCurrentLicense(self):
        has = not (self._currentLicense is None)
        return has

    # Code from template association_GetMany 
    def getTestRecord(self, index):
        aTestRecord = self._testRecords[index]
        return aTestRecord

    #*
    
    #   * Every stored test record belongs to exactly one applicant.
    
    #   
    def getTestRecords(self):
        newTestRecords = tuple(self._testRecords)
        return newTestRecords

    def numberOfTestRecords(self):
        number = len(self._testRecords)
        return number

    def hasTestRecords(self):
        has = len(self._testRecords) > 0
        return has

    def indexOfTestRecord(self, aTestRecord):
        index = (-1 if not aTestRecord in self._testRecords else self._testRecords.index(aTestRecord))
        return index

    # Code from template association_SetOptionalOneToOne 
    def setCurrentLicense(self, aNewCurrentLicense):
        wasSet = False
        if not (self._currentLicense is None) and not self._currentLicense == aNewCurrentLicense and self == self._currentLicense.getApplicant() :
            #Unable to setCurrentLicense, as existing currentLicense would become an orphan
            return wasSet
        self._currentLicense = aNewCurrentLicense
        anOldApplicant = (aNewCurrentLicense.getApplicant()) if not (aNewCurrentLicense is None) else None
        if not self == anOldApplicant :
            if not (anOldApplicant is None) :
                anOldApplicant.currentLicense = None
            if not (self._currentLicense is None) :
                self._currentLicense.setApplicant(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfTestRecords():
        return 0

    # Code from template association_AddManyToOne 
    def addTestRecord1(self, aRecordId, aScore):
        from Reproduction.DriverLicense.TestRecord import TestRecord
        return TestRecord(aRecordId, aScore, self)

    def addTestRecord2(self, aTestRecord):
        wasAdded = False
        if (aTestRecord) in self._testRecords :
            return False
        existingApplicant = aTestRecord.getApplicant()
        isNewApplicant = not (existingApplicant is None) and not self == existingApplicant
        if isNewApplicant :
            aTestRecord.setApplicant(self)
        else :
            self._testRecords.append(aTestRecord)
        wasAdded = True
        return wasAdded

    def removeTestRecord(self, aTestRecord):
        wasRemoved = False
        #Unable to remove aTestRecord, as it must always have a applicant
        if not self == aTestRecord.getApplicant() :
            self._testRecords.remove(aTestRecord)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addTestRecordAt(self, aTestRecord, index):
        wasAdded = False
        if self.addTestRecord(aTestRecord) :
            if index < 0 :
                index = 0
            if index > self.numberOfTestRecords() :
                index = self.numberOfTestRecords() - 1
            self._testRecords.remove(aTestRecord)
            self._testRecords.insert(index, aTestRecord)
            wasAdded = True
        return wasAdded

    def addOrMoveTestRecordAt(self, aTestRecord, index):
        wasAdded = False
        if (aTestRecord) in self._testRecords :
            if index < 0 :
                index = 0
            if index > self.numberOfTestRecords() :
                index = self.numberOfTestRecords() - 1
            self._testRecords.remove(aTestRecord)
            self._testRecords.insert(index, aTestRecord)
            wasAdded = True
        else :
            wasAdded = self.addTestRecordAt(aTestRecord, index)
        return wasAdded

    def delete(self):
        Applicant.applicantsByApplicantId.pop(self.getApplicantId(), None)
        existingCurrentLicense = self._currentLicense
        self._currentLicense = None
        if not (existingCurrentLicense is None) :
            existingCurrentLicense.delete()
        i = len(self._testRecords)
        while i > 0 :
            aTestRecord = self._testRecords[i - 1]
            aTestRecord.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "applicantId" + ":" + str(self.getApplicantId()) + "," + "nameCode" + ":" + str(self.getNameCode()) + "," + "birthYear" + ":" + str(self.getBirthYear()) + "," + "addressCode" + ":" + str(self.getAddressCode()) + "," + "feePaid" + ":" + str(self.getFeePaid()) + "," + "lastScore" + ":" + str(self.getLastScore()) + "," + "suspensionCode" + ":" + str(self.getSuspensionCode()) + "]" + str(os.linesep) + "  " + "currentLicense = " + ((format(id(self.getCurrentLicense()), "x")) if not (self.getCurrentLicense() is None) else "null")

    def addTestRecord(self, *argv):
        from Reproduction.DriverLicense.TestRecord import TestRecord
        if len(argv) == 2 and isinstance(argv[0], int) and isinstance(argv[1], int) :
            return self.addTestRecord1(argv[0], argv[1])
        if len(argv) == 1 and isinstance(argv[0], TestRecord) :
            return self.addTestRecord2(argv[0])
        raise TypeError("No method matches provided parameters")

