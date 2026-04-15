from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parents[1]
PYTHON_GEN_DIR = BASE_DIR / "models" / "generated" / "python"
sys.path.insert(0, str(PYTHON_GEN_DIR))

from Reproduction.DriverLicense.Applicant import Applicant
from Reproduction.DriverLicense.DrivingLicense import DrivingLicense


def snapshot(label: str, applicant: Applicant) -> None:
    current_license = applicant.getCurrentLicense()
    license_number = current_license.getLicenseNumber() if current_license else None
    print(
        f"{label}: state={applicant.getLicenseLifecycleFullName()}, "
        f"feePaid={applicant.getFeePaid()}, "
        f"lastScore={applicant.getLastScore()}, "
        f"suspensionCode={applicant.getSuspensionCode()}, "
        f"currentLicense={license_number}, "
        f"testRecords={applicant.numberOfTestRecords()}"
    )


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    applicant = Applicant(1)
    snapshot("initial", applicant)
    expect(applicant.getLicenseLifecycleFullName() == "NoLicense", "initial state mismatch")

    expect(applicant.payFee(), "payFee should be accepted in NoLicense")
    expect(applicant.passG1Test(), "passG1Test should succeed after paying the fee")
    applicant.addTestRecord(1001, 80)
    current_license = DrivingLicense(5001, applicant)
    current_license.setKindCode(1)
    snapshot("after_g1", applicant)
    expect(applicant.getLicenseLifecycleFullName() == "Licensed.G1", "G1 transition failed")

    expect(applicant.payFee(), "payFee should be accepted in G1")
    expect(applicant.passG2Test(), "passG2Test should succeed after paying the fee")
    applicant.addTestRecord(1002, 82)
    current_license.setKindCode(2)
    snapshot("after_g2", applicant)
    expect(applicant.getLicenseLifecycleFullName() == "Licensed.G2", "G2 transition failed")

    expect(applicant.payFee(), "payFee should be accepted in G2")
    expect(applicant.passGTest(), "passGTest should succeed after paying the fee")
    applicant.addTestRecord(1003, 88)
    current_license.setKindCode(3)
    snapshot("after_g", applicant)
    expect(applicant.getLicenseLifecycleFullName() == "Licensed.G", "G transition failed")

    expect(applicant.suspend(), "suspend should be accepted in G")
    snapshot("after_suspend", applicant)
    expect(applicant.getLicenseLifecycleFullName() == "Suspended", "suspended state mismatch")
    expect(applicant.getSuspensionCode() == 3, "suspension code for G should be 3")

    expect(applicant.reinstateAsG(), "reinstateAsG should succeed from a G suspension")
    snapshot("after_reinstate", applicant)
    expect(applicant.getLicenseLifecycleFullName() == "Licensed.G", "reinstate to G failed")

    expect(applicant.expire(), "expire should be accepted in G")
    snapshot("after_expire", applicant)
    expect(applicant.getLicenseLifecycleFullName() == "ExpiredG", "expired G state mismatch")

    expect(applicant.renewG(), "renewG should succeed from ExpiredG")
    snapshot("after_renew", applicant)
    expect(applicant.getLicenseLifecycleFullName() == "Licensed.G", "renewal back to G failed")
    expect(applicant.numberOfTestRecords() == 3, "expected three recorded tests")
    expect(applicant.getCurrentLicense().getLicenseNumber() == 5001, "license association mismatch")

    print("python_demo_ok")


if __name__ == "__main__":
    main()
