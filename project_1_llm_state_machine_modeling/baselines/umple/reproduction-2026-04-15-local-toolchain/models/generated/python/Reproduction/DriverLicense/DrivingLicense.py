#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8531.81852a8bc modeling language!
# line 81 "../../driver_license_system.ump"
import os

class DrivingLicense():
    drivinglicensesByLicenseNumber = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #DrivingLicense Attributes
    #DrivingLicense Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aLicenseNumber, aApplicant):
        self._applicant = None
        self._kindCode = None
        self._issuedYear = None
        self._licenseNumber = None
        self._issuedYear = 2026
        self._kindCode = 3
        if not self.setLicenseNumber(aLicenseNumber) :
            raise RuntimeError ("Cannot create due to duplicate licenseNumber. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        didAddApplicant = self.setApplicant(aApplicant)
        if not didAddApplicant :
            raise RuntimeError ("Unable to create currentLicense due to applicant. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setLicenseNumber(self, aLicenseNumber):
        wasSet = False
        anOldLicenseNumber = self.getLicenseNumber()
        if not (anOldLicenseNumber is None) and anOldLicenseNumber == aLicenseNumber :
            return True
        if DrivingLicense.hasWithLicenseNumber(aLicenseNumber) :
            return wasSet
        self._licenseNumber = aLicenseNumber
        wasSet = True
        if not (anOldLicenseNumber is None) :
            DrivingLicense.drivinglicensesByLicenseNumber.pop(anOldLicenseNumber, None)
        DrivingLicense.drivinglicensesByLicenseNumber[aLicenseNumber] = self
        return wasSet

    def setIssuedYear(self, aIssuedYear):
        wasSet = False
        self._issuedYear = aIssuedYear
        wasSet = True
        return wasSet

    def setKindCode(self, aKindCode):
        wasSet = False
        self._kindCode = aKindCode
        wasSet = True
        return wasSet

    def getLicenseNumber(self):
        return self._licenseNumber

    # Code from template attribute_GetUnique 
    @staticmethod
    def getWithLicenseNumber(aLicenseNumber):
        return DrivingLicense.drivinglicensesByLicenseNumber.get(aLicenseNumber)

    # Code from template attribute_HasUnique 
    @staticmethod
    def hasWithLicenseNumber(aLicenseNumber):
        return not (DrivingLicense.getWithLicenseNumber(aLicenseNumber) is None)

    def getIssuedYear(self):
        return self._issuedYear

    def getKindCode(self):
        return self._kindCode

    # Code from template association_GetOne 
    def getApplicant(self):
        return self._applicant

    # Code from template association_SetOneToOptionalOne 
    def setApplicant(self, aNewApplicant):
        wasSet = False
        if aNewApplicant is None :
            #Unable to setApplicant to null, as currentLicense must always be associated to a applicant
            return wasSet
        existingCurrentLicense = aNewApplicant.getCurrentLicense()
        if not (existingCurrentLicense is None) and not self == existingCurrentLicense :
            #Unable to setApplicant, the current applicant already has a currentLicense, which would be orphaned if it were re-assigned
            return wasSet
        anOldApplicant = self._applicant
        self._applicant = aNewApplicant
        self._applicant.setCurrentLicense(self)
        if not (anOldApplicant is None) :
            anOldApplicant.setCurrentLicense(None)
        wasSet = True
        return wasSet

    def delete(self):
        DrivingLicense.drivinglicensesByLicenseNumber.pop(self.getLicenseNumber(), None)
        existingApplicant = self._applicant
        self._applicant = None
        if not (existingApplicant is None) :
            existingApplicant.setCurrentLicense(None)

    def __str__(self):
        return str(super().__str__()) + "[" + "licenseNumber" + ":" + str(self.getLicenseNumber()) + "," + "issuedYear" + ":" + str(self.getIssuedYear()) + "," + "kindCode" + ":" + str(self.getKindCode()) + "]" + str(os.linesep) + "  " + "applicant = " + ((format(id(self.getApplicant()), "x")) if not (self.getApplicant() is None) else "null")

