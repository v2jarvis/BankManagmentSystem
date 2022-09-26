import sqlite3 as sql
import sys
import os
import datetime as dt
con=sql.connect("bankDB")
table1="create table if not exists customer(accountno int,name varchar(50),gender varchar(10),email varchar(30),phone bigint,acc_type varchar(20),balance_amnt int,active int,primary key(accountno))"
table2="create table if not exists transaction1(accountno int,t_type varchar(20),t_date datetime,amount int)"
cur=con.cursor()
cur.execute(table1)
cur.execute(table2)

def CreateAccount():
    ano=int(input("Enter Account Number : "))
    name=input("Enter Account Holder Name : ")
    gender=input("Enter Account Holder Gender : ")
    email=input("Enter Account Holder Email Id : ")
    phone=int(input("Enter Phone Number : "))
    op1=int(input("Enter 1 For Saving Account And 2 For Current Account : "))
    if op1==1:
        atype="Saving"
    elif op1==2:
        atype="Current"
    else:
        print("Invalid Choice!!! ")
    amount=int(input("Enter Ammont To Deposite : "))
    qry="insert into customer values(%d,'%s','%s','%s',%d,'%s',%d,%d)"%(ano,name,gender,email,phone,atype,amount,1)
    try:
        cur.execute(qry)
    except sql.IntegrityError:
        print("Duplicate Account Number!!!")
    else:
        if cur.rowcount>0:
            print("Account Created !!! ")
        else:
            print("Error in creating the account !! ")
        con.commit()

def ViewAllAccount():
    print("-"*108)
    print("%7s %25s %8s %30s %12s %8s %10s" %("A\cNo","Name","Gender","Email","PhoneNo","Type","Ammount"))
    print("-"*108)
    qry="select * from customer"
    cur.execute(qry)
    for i in cur.fetchall():
        print("%7s %25s %8s %30s %12s %8s %10s"%(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
        print("-"*108)

def EditAccount():
    accno=int(input("Enter Account number"))
    qry="select * from customer where accountno=%d"%(accno)
    cur.execute(qry)
    result=cur.fetchall()
    if len(result)>0:
        print("1 Name")
        print("2 gender")
        print("3 Email ID")
        print("4 Phone Number")
        ch=int(input("Enter choice to modify the record:"))
        if ch==1:
            name=input("Enter New Name:")
            qry="update customer set name='%s' where accountno=%d"%(name,accno)
        elif ch==2:
            gen=input("Enter gender:")
            qry="update customer set gender='%s' where accountno=%d"%(gen,accno)
        elif ch==3:
            email=input("Enter New Email ID:")
            qry="update customer set email='%s' where accountno=%d"%(email,accno)
        elif ch==4:
            phone=input("Enter New Phone Number:")
            qry="update customer set phone='%s' where accountno=%d"%(phone,accno)
        else:
            print("Invalid Choice")
        if ch>=1 and ch<=4:
            cur.execute(qry)
            if cur.rowcount>0:
                print("Record Updated")
            con.commit()
        else:
                print("Error in updating the record")
    else:
        print("Invalid Account Number")
            
def DepositAmount():
    ano=int(input("Enter Account Number:"))
    qry="select balance_amnt from customer where accountno=%d"%(ano)
    cur.execute(qry)
    result=cur.fetchall()
    if len(result)>0:
       amount=result[0][0]
       damount=int(input("Enter Amount To deposit:"))
       qry="update customer set balance_amnt=%d where accountno=%d"%(amount+damount,ano)
       cur.execute(qry)
       qry="insert into transaction1 values(%d,'%s','%s',%d)"%(ano,"credit",dt.datetime.now(),damount)
       cur.execute(qry)
       if cur.rowcount>0:
            print("Amount is Credited!!!")
       else:
           print("Error in crediting the amount")
       con.commit()
    else:
         print("Invalid Account Number")

def WithdrawAmount():
    ano=int(input("Enter Account Number:"))
    qry="select balance_amnt from customer where accountno=%d"%(ano)
    cur.execute(qry)
    result=cur.fetchall()
    if len(result)>0:
       amount=result[0][0]
       wamount=int(input("Enter Amount To Withdraw:"))
       if wamount<=amount:
           qry="update customer set balance_amnt=%d where accountno=%d"%(amount-wamount,ano)
           cur.execute(qry)
           qry="insert into transaction1 values(%d,'%s','%s',%d)"%(ano,"debit",dt.datetime.now(),wamount)
           cur.execute(qry)
           if cur.rowcount>0:
                print("Amount is Withdraw!!!")
           else:
                print("Error in Crediting the amount")
       con.commit()
    else:
         print("Invalid Account Number")
         
def ShowBalance():
    ano=int(input("Enter Account Number:"))
    qry="select balance_amnt from customer where accountno=%d"%(ano)
    cur.execute(qry)
    result=cur.fetchall()
    if len(result)>0:
       amount=result[0][0]
       print("Total Amount=",amount)
    else:
       print("Invalid Account Number")
    
def MiniStatement():
    ano=int(input("Enter Account Number:"))
    qry="select * from transaction1 where accountno=%d"%(ano)
    cur.execute(qry)
    result=cur.fetchall()
    if len(result)>0:
        print("-"*90)
        print("%7s %10s %15s %10s %10s"%("A/c No","Type","Date","Time","Amount"))
        print("-"*90)
        for i in result:
            date=i[2][0:10]
            time=i[2][11:19]
            print("%7d %10s %15s %10s %10d"%(i[0],i[1],date,time,i[3]))
            print("-"*90)
    else:
        print("No Transaction Found...")
        
def CloseAccount():
        accno=int(input("Enter Account Number: "))
        qry="select * from customer where accountno=%d"%(accno)
        cur.execute(qry)
        result=cur.fetchall()
        if len(result)>0:
            qry="update customer set active=0 where accountno=%d"%(accno)
            cur.execute(qry)
            con.commit()
            print("\nAccount Close Successfully")
        else:
            print("Invalid Account Number")
        con.commit()

def MoneyTransfer():
        acno1=int(input("From Account : "))
        qry="select balance_amnt from customer where accountno=%d"%(acno1)
        cur.execute(qry)
        result1=cur.fetchall()
        if len(result1)>0:
            amount1=result1[0][0]
        else:
            print("Invalid Account Number!!!")
        
        acno2=int(input("To Account : "))
        qry="select balance_amnt from customer where accountno=%d"%(acno2)
        cur.execute(qry)
        result2=cur.fetchall()
        if len(result2)>0:
            amount2=result2[0][0]
            trnsmoney=int(input("Enter Transfer Amount : "))
            if trnsmoney<=amount1:         
                amount1=amount1-trnsmoney
                amount2=amount2+trnsmoney
                qry1="update customer set balance_amnt=%d where accountno=%d"%(amount1,acno1)      
                cur.execute(qry1)
                qry2="update customer set balance_amnt=%d where accountno=%d"%(amount2,acno2)      
                cur.execute(qry2)
                qry="insert into transaction1 values(%d,'%s','%s',%d)"%(acno1,"Dr.",dt.datetime.now(),trnsmoney)
                cur.execute(qry)
                qry="insert into transaction1 values(%d,'%s','%s',%d)"%(acno2,"Cr.",dt.datetime.now(),trnsmoney)
                cur.execute(qry)
            else:
                print("Balance is Low")
            if cur.rowcount>0:
                print("\nTransfer  Successful !!!")
            else:
                print("\nError on Transfering")

        else:
            print("\nInvalid Account Number!!!")
        
        con.commit()    
        
while True:
    os.system("cls")
    print("\nBanking Management System\n")
    print("1. Create New Account")
    print("2. Deposite Ammount")
    print("3. Withdraw Ammount")
    print("4. Balance Enquiry")
    print("5. View All Account Holder")
    print("6. Modify An Account")
    print("7. Mini Statement")
    print("8. Close An Account")
    print("9. Money Transfer")
    print("10. Exit")
    choice=int(input("Enter Choice : "))
    if choice==1:
        CreateAccount()
        os.system("pause")
    elif choice==2:
        DepositAmount()
        os.system("pause")
    elif choice==3:
        WithdrawAmount()
        os.system("pause")
    elif choice==4:
        ShowBalance()
        os.system("pause")
    elif choice==5:
        ViewAllAccount()
        os.system("pause")
    elif choice==6:
        EditAccount()
        os.system("pause")
    elif choice==7:
        MiniStatement()
        os.system("pause")
    elif choice==8:
        CloseAccount()
        os.system("pause")
    elif choice==9:
        MoneyTransfer()
        os.system("pause")
    elif choice==10:
        pass
    else:
        print("Invalid Choice !!! ")
        
