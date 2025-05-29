public class AccountTriggerHandler {
    public static void handleAfterInsert(List<Account> newAccounts) {
        List<Contact> contactsToInsert = new List<Contact>();
        
        for (Account acc : newAccounts) {
            if (String.isNotBlank(acc.Name)) {
                Contact con = new Contact();
                con.FirstName ='CF';
                con.LastName = acc.Name;
                con.AccountId = acc.Id;
                con.Phone=acc.phone;
                contactsToInsert.add(con);
            }
        }
        
        if (!contactsToInsert.isEmpty()) {
            insert contactsToInsert;
        }
    }


}