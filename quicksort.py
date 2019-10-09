
list_before=[2,4,9,3,4,5,2,1,5,6,4,2,7,8,6,0]
def quickSort1(list_before):
    if len(list_before)<2:
        return list_before

    midprivot=list_before[len(list_before)//2]  # 以中间元素作为基准
    
    left_part=[x for x in list_before if x<midprivot]
    right_part=[y for y in list_before if y>midprivot]
    standard_point=[z for z in list_before if z==midprivot ]
    
    return quickSort1(left_part)+standard_point+quickSort1(right_part)

print(quickSort1(list_before))

def quickSort2(list_before):
    if len(list_before)<2:
        return list_before
    
    # 以列表中的第一个元素为基准
    # list_before[0:1] 是一个列表,可以与其他列表进行+运算
    return quickSort2([left_ele for left_ele in list_before[1:] if left_ele<list_before[0]])+list_before[0:1]+quickSort2([right_ele for right_ele in list_before[1:] if right_ele>=list_before[0]])

print(quickSort2(list_before))
