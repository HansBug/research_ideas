#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8531.81852a8bc modeling language!
# line 90 "../../driver_license_system.ump"
import os

class TestRecord():
    testrecordsByRecordId = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #TestRecord Attributes
    #TestRecord Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aRecordId, aScore, aApplicant):
        self._applicant = None
        self._passCode = None
        self._score = None
        self._testTypeCode = None
        self._recordId = None
        self._testTypeCode = 1
        self._score = aScore
        self._passCode = 1
        if not self.setRecordId(aRecordId) :
            raise RuntimeError ("Cannot create due to duplicate recordId. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        didAddApplicant = self.setApplicant(aApplicant)
        if not didAddApplicant :
            raise RuntimeError ("Unable to create testRecord due to applicant. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setRecordId(self, aRecordId):
        wasSet = False
        anOldRecordId = self.getRecordId()
        if not (anOldRecordId is None) and anOldRecordId == aRecordId :
            return True
        if TestRecord.hasWithRecordId(aRecordId) :
            return wasSet
        self._recordId = aRecordId
        wasSet = True
        if not (anOldRecordId is None) :
            TestRecord.testrecordsByRecordId.pop(anOldRecordId, None)
        TestRecord.testrecordsByRecordId[aRecordId] = self
        return wasSet

    def setTestTypeCode(self, aTestTypeCode):
        wasSet = False
        self._testTypeCode = aTestTypeCode
        wasSet = True
        return wasSet

    def setScore(self, aScore):
        wasSet = False
        self._score = aScore
        wasSet = True
        return wasSet

    def setPassCode(self, aPassCode):
        wasSet = False
        self._passCode = aPassCode
        wasSet = True
        return wasSet

    def getRecordId(self):
        return self._recordId

    # Code from template attribute_GetUnique 
    @staticmethod
    def getWithRecordId(aRecordId):
        return TestRecord.testrecordsByRecordId.get(aRecordId)

    # Code from template attribute_HasUnique 
    @staticmethod
    def hasWithRecordId(aRecordId):
        return not (TestRecord.getWithRecordId(aRecordId) is None)

    def getTestTypeCode(self):
        return self._testTypeCode

    def getScore(self):
        return self._score

    def getPassCode(self):
        return self._passCode

    # Code from template association_GetOne 
    def getApplicant(self):
        return self._applicant

    # Code from template association_SetOneToMany 
    def setApplicant(self, aApplicant):
        wasSet = False
        if aApplicant is None :
            return wasSet
        existingApplicant = self._applicant
        self._applicant = aApplicant
        if not (existingApplicant is None) and not existingApplicant == aApplicant :
            existingApplicant.removeTestRecord(self)
        self._applicant.addTestRecord(self)
        wasSet = True
        return wasSet

    def delete(self):
        TestRecord.testrecordsByRecordId.pop(self.getRecordId(), None)
        placeholderApplicant = self._applicant
        self._applicant = None
        if not (placeholderApplicant is None) :
            placeholderApplicant.removeTestRecord(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "recordId" + ":" + str(self.getRecordId()) + "," + "testTypeCode" + ":" + str(self.getTestTypeCode()) + "," + "score" + ":" + str(self.getScore()) + "," + "passCode" + ":" + str(self.getPassCode()) + "]" + str(os.linesep) + "  " + "applicant = " + ((format(id(self.getApplicant()), "x")) if not (self.getApplicant() is None) else "null")

