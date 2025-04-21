class :BankAccount {
    :__accountNumber = 12345678   
    :balance = 0               

    def getBalance(:self) {
        return :self.:balance
    }

    def deposit(:self, :amt) {
        :self.:balance = :self.:balance + :amt
        return 0
    }

    def withdraw(:self, :amt) {
        if :self.:balance >= :amt [
            :self.:balance = :self.:balance - :amt
            return 0
        ]
        else [
            return -1
        ]
    }
}


class :SavingsAccount(:BankAccount) {
    :__interestRate = 0.05       

  
    def withdraw(:self, :amt) {
        if :self.:balance >= :amt [
            :self.:balance = :self.:balance - :amt
            return 0
        ]
        else [
            return -1
        ]
    }

    def addInterest(:self) {
        :interest = :self.:balance * :self.:__interestRate
        :self.:balance = :self.:balance + :interest
        return 0
    }
}


class :CheckingAccount(:BankAccount) {
    :__overdraftLimit = 500


    def withdraw(:self, :amt) {
        if :self.:balance + :self.:__overdraftLimit >= :amt [
            :self.:balance = :self.:balance - :amt
            return 0
        ]
        else [
            return -1
        ]
    }
}


:saveAcc = new :SavingsAccount()
:saveAcc.deposit(1000)
:saveAcc.addInterest()
:bal1 = :saveAcc.getBalance()
print(:bal1)          

:chkAcc = new :CheckingAccount()
:chkAcc.deposit(200)
:chkAcc.withdraw(600) 
:bal2 = :chkAcc.getBalance()
print(:bal2)