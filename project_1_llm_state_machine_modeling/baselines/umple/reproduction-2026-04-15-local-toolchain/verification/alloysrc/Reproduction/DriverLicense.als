module Reproduction/DriverLicense

------------------------------------------------------------------------------------------------------------------

-- This Alloy file is generated using Umple from driver_license_system.ump

------------------------------------------------------------------------------------------------------------------


-- Defines a signature for class Applicant
sig Applicant {
  currentLicense : lone DrivingLicense,
  testRecords : set TestRecord,
  applicantId : Int,
  nameCode : Int,
  birthYear : Int,
  addressCode : Int,
  feePaid : Int,
  lastScore : Int,
  suspensionCode : Int
}

-- Defines a signature for class DrivingLicense
sig DrivingLicense {
  applicant : one Applicant,
  licenseNumber : Int,
  issuedYear : Int,
  kindCode : Int
}

-- Defines a signature for class TestRecord
sig TestRecord {
  applicant : one Applicant,
  recordId : Int,
  testTypeCode : Int,
  score : Int,
  passCode : Int
}


-- Defines constraints on association between DrivingLicense and Applicant
fact AssociationFact {
  DrivingLicense <: applicant in (DrivingLicense) lone -> lone (Applicant)
}

-- Defines constraints on association between TestRecord and Applicant
fact AssociationFact {
  TestRecord <: applicant in (TestRecord) set -> set (Applicant)
}

-- Defines bidirectionality rule between class Applicant and class DrivingLicense
fact BidirectionalityRule {
  all applicant_1 : Applicant, drivinglicense_1 : DrivingLicense |
    applicant_1 in applicant[drivinglicense_1] <=> drivinglicense_1 in currentLicense[applicant_1]
}

-- Defines bidirectionality rule between class Applicant and class TestRecord
fact BidirectionalityRule {
  all applicant_1 : Applicant, testrecord_1 : TestRecord |
    applicant_1 in applicant[testrecord_1] <=> testrecord_1 in testRecords[applicant_1]
}