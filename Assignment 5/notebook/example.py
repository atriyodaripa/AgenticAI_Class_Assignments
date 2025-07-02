from typing import Literal

def grade_documents(a:int, b:int) -> Literal["Output Generator", "Query Rewriter"]:
    if a * b==15:
        return "reviewer"
    else:
        return "rewriter"
    
print(grade_documents(3,5))