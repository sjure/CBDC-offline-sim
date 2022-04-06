

def traverse_backwards(payment_number, visited_payments, stack, payment_address_map, payments):
    visited_payments[payment_number] = True

    for i in payment_address_map[payments[payment_number].tx.from_address]:
        if not visited_payments[i]:
            traverse_backwards(i, visited_payments, stack,
                               payment_address_map, payments)

    stack.append(payments[payment_number])


def sort_payments(payments):
    visited_payments = [False]*len(payments)
    stack = []
    payment_address_map = {}
    for payment_number, payment in enumerate(payments):
        if payment.tx.from_address in payment_address_map.keys():
            payment_address_map[payment.tx.from_address].append(
                (payment_number, payment.tx.counter))
        else:
            payment_address_map[payment.tx.from_address] = [
                (payment_number, payment.tx.counter)]

    # Sort each user outbound edge after counter
    for address in payment_address_map.keys():
        payment_address_map[address].sort(
            key=lambda x: x[1])
        payment_address_map[address] = [i[0]
                                        for i in payment_address_map[address]]
    for i in range(len(payments)):
        if not visited_payments[i]:
            traverse_backwards(i, visited_payments, stack,
                               payment_address_map, payments)
    return stack[::-1]
