import sys
import os
import csv
import io
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

data = """Nama Lengkap,NIM,Program Studi,Semester,Keahlian/Fokus utama kamu saat ini?,email,Role
Superadmin,1010511000,Admin,0,Admin,aiot@upnvj.ac.id,Admin
Rahman Ilyas Al Kahfi,2210511044,S1 Informatika,8,Artificial Intelligence / Machine Learning,2210511044@mahasiswa.upnvj.ac.id,Mentor
Adinda Rizki Sya'bana Diva,2210511056,S1 Informatika,8,Artificial Intelligence / Machine Learning,2210511056@mahasiswa.upnvj.ac.id,Mentor
Nicolas Debrito,2210511057,S1 Informatika,8,Artificial Intelligence / Machine Learning,2210511057@mahasiswa.upnvj.ac.id,Mentor
Yusuf Martinus Arief,2210511081,S1 Informatika,8,Internet of Things (IoT),2210511081@mahasiswa.upnvj.ac.id,Mentor
Dzulfikri Adjmal,2210511084,S1 Informatika,8,Artificial Intelligence / Machine Learning,2210511084@mahasiswa.upnvj.ac.id,Mentor
Bima Saputra,2310511042,S1 Informatika,6,Internet of Things (IoT),2310511042@mahasiswa.upnvj.ac.id,Mentor
Clara Ragil Dewanti,2410501116,D3 Sistem Informasi,4,Artificial Intelligence / Machine Learning,2410501116@mahasiswa.upnvj.ac.id,Member
Gizza Anandita Fallah,2410501127,D3 Sistem Informasi,4,Artificial Intelligence / Machine Learning,2410501127@mahasiswa.upnvj.ac.id,Member
Bunga citra nur fadilla,2410511075,S1 Informatika,4,Web & Cloud Systems,2410511075@mahasiswa.upnvj.ac.id,Member
Muhammad Khalif,2410511122,S1 Informatika,4,Internet of Things (IoT),2410511122@mahasiswa.upnvj.ac.id,Member
Mohammad Yomandiguna Zakaria,2410511130,S1 Informatika,4,Internet of Things (IoT),2410511130@mahasiswa.upnvj.ac.id,Member
Naufal Rizky Ramadhan,2410511160,S1 Informatika,4,Web & Cloud Systems,2410511160@mahasiswa.upnvj.ac.id,Member
Atilla Majid Hartono,2510501023,D3 Sistem Informasi,2,Artificial Intelligence / Machine Learning,2510501023@mahasiswa.upnvj.ac.id,Member
Dimaz Azriel Prayayewa,2510501033,D3 Sistem Informasi,2,Artificial Intelligence / Machine Learning,2510501033@mahasiswa.upnvj.ac.id,Member
Nur Izzati Zafira,2510511041,S1 Informatika,2,Web & Cloud Systems,2510511041@mahasiswa.upnvj.ac.id,Member
Hanif Naundra Arsantyo,2510511077,S1 Informatika,2,Web & Cloud Systems,2510511077@mahasiswa.upnvj.ac.id,Member
Raya Destrya Inamori,2510511097,S1 Informatika,2,Internet of Things (IoT),2510511097@mahasiswa.upnvj.ac.id,Member
Feby Valentine Samosir,2510511099,S1 Informatika,2,Internet of Things (IoT),2510511099@mahasiswa.upnvj.ac.id,Member
Rehanaya Syahfitri,2510511107,S1 Informatika,2,Internet of Things (IoT),2510511107@mahasiswa.upnvj.ac.id,Member
Muhammad Azzam Al Hannan,2510511114,S1 Informatika,2,Web & Cloud Systems,2510511114@mahasiswa.upnvj.ac.id,Member
Arsy Maulana Sidiq,2510511119,S1 Informatika,2,Artificial Intelligence / Machine Learning,2510511119@mahasiswa.upnvj.ac.id,Member
Fairuz Mumtaziyah Gornea,2510511132,S1 Informatika,2,Web & Cloud Systems,2510511132@mahasiswa.upnvj.ac.id,Member
Aniqah Raniah Ramadhani Lakare,2510511141,S1 Informatika,2,Artificial Intelligence / Machine Learning,2510511141@mahasiswa.upnvj.ac.id,Member
Septi Astuti,2510511142,S1 Informatika,2,Internet of Things (IoT),2510511142@mahasiswa.upnvj.ac.id,Member
Alfred Yosua,2510511146,S1 Informatika,2,Web & Cloud Systems,2510511146@mahasiswa.upnvj.ac.id,Member
Yoram Messiah Kaliey,2510511153,S1 Informatika,2,Internet of Things (IoT),2510511153@mahasiswa.upnvj.ac.id,Member
Farrel Shanrui Fikri,2510511160,S1 Informatika,2,Web & Cloud Systems,2510511160@mahasiswa.upnvj.ac.id,Member
Stenly Christian,2510511162,S1 Informatika,2,Web & Cloud Systems,2510511162@mahasiswa.upnvj.ac.id,Member
Ihsan Naufal Ikhwansyah,2510511168,S1 Informatika,2,Web & Cloud Systems,2510511168@mahasiswa.upnvj.ac.id,Member
Ramadhania,2510511171,S1 Informatika,2,Web & Cloud Systems,2510511171@mahasiswa.upnvj.ac.id,Member
Farel muhammad nelwan,2510511172,S1 Informatika,2,Internet of Things (IoT),2510511172@mahasiswa.upnvj.ac.id,Member
Levianto Adhigana Putra,2510511175,S1 Informatika,2,Internet of Things (IoT),2510511175@mahasiswa.upnvj.ac.id,Member
Marvellyn Gracia Silalahi,2510511180,S1 Informatika,2,Artificial Intelligence / Machine Learning,2510511180@mahasiswa.upnvj.ac.id,Member
Muhammad Mulia Wahiddin Harahap,2510512008,S1 Sistem Informasi,2,Artificial Intelligence / Machine Learning,2510512008@mahasiswa.upnvj.ac.id,Member"""

def import_users():
    reader = csv.DictReader(io.StringIO(data))

    db = SessionLocal()
    added_count = 0
    updated_count = 0
    
    for row in reader:
        email = str(row['email']).strip()
        role = str(row.get('Role', 'Member')).strip().upper()
        if role not in ["ADMIN", "MENTOR", "MEMBER"]:
            role = "MEMBER"
            
        if role == "ADMIN":
            raw_password = "six faced world"
        elif role == "MENTOR":
            raw_password = "pleiades"
        else:
            raw_password = "aiotupnvj2026"
            
        hashed_password = get_password_hash(raw_password)
        existing_user = db.query(User).filter(User.email == email).first()
        
        nim = str(row.get('NIM'))
        semester = str(row.get('Semester'))
        
        if existing_user:
            print(f"Updating existing user: {email}")
            existing_user.name = row['Nama Lengkap']
            existing_user.nim = nim
            existing_user.program_studi = row.get('Program Studi')
            existing_user.semester = semester
            existing_user.interest = row.get('Keahlian/Fokus utama kamu saat ini?')
            existing_user.role = role
            existing_user.password_hash = hashed_password
            updated_count += 1
        else:
            print(f"Adding new user: {email}")
            new_user = User(
                email=email,
                name=row['Nama Lengkap'],
                nim=nim,
                program_studi=row.get('Program Studi'),
                semester=semester,
                interest=row.get('Keahlian/Fokus utama kamu saat ini?'),
                role=role,
                password_hash=hashed_password
            )
            db.add(new_user)
            added_count += 1
            
    db.commit()
    db.close()
    print(f"Import completed! Added: {added_count}, Updated: {updated_count}")

if __name__ == "__main__":
    import_users()
