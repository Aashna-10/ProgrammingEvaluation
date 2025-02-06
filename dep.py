from openai import OpenAI
def get_completion(prompt):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "developer", "content": "You are a assistant specializing in computer science, particularly evaluation of code. Whenever you are given a task you reason clearly and unambiguously to arrive at an answer. Instead of rushing to an answer you think the problem through even if it takes more time than usual. You are not too verbose. Your answers are short with all the necessary information included. If you do not know the answer of a particular question you simply reply with 'I do not know'"},
        {"role": "user", "content": prompt}
    ]
    )
    return (completion.choices[0].message.content)
def getDepth(code):
    # get the depth of the code
    # return the depth
    prompt=f"get the depth of the code delimited by triple backticks. Depth of the code is defined as nesting level of predefined constructs. The constructs that are considered as a new level are as follows:- a loop, assignment of a variable, defining a class, defining a function/method, a conditional using if-else or a switch call. Return a single number - the depth of the given code. Do not attach any pre or post text like depth is etc.  ```{code}```"
    ans = get_completion(prompt)
    return int(ans)

def codeDecomposition(code):
    # break code into subcodes using AST. ast in python can only be used for python files. check clang for c/c++ files
    # suggested by chatGPT
    # return a list of the subcodes
def getDependencies(code):
    # get the dependencies of the code
    # return a list of dependencies
def retrieveSemantics(dependencies):
    # get the semantics of the dependencies
    # return a dictionary of the dependencies and their semantics
def LLM(code,dependencies,subCodesSemantics=None):
    # use the LLM to get the semantics of the code
    # return the semantics of the code
def updateSemantic(dependency,subCodesSemantic):
    # update the semantic of the dependency using the semantic of the subcodes
    # return the updated semantic
def summarizeSemantic(subCodesSemantics):
    # summarize the semantics of the subcodes
    # return the summarized semantic

    
def getSemantic(code):
    storage={}
    subCodes=codeDecomposition(code)
    subCodesSemantics=[]
    for SC in subCodes:
        SCDepth=getDepth(SC)
        dependencies=getDependencies(SC)
        dependencySemantics=retrieveSemantics(dependencies)
        if SCDepth<3:
            subCodesSemantic=LLM(SC,dependencySemantics)
        else:
            SSCSemantics=getSemantic(SC)
            subCodesSemantic=LLM(SC,dependencySemantics,SSCSemantics)
        subCodesSemantics.append(subCodesSemantic)
        for DP in dependencySemantics:
            newDependency=updateSemantic(DP,subCodesSemantic)
            storage.update(newDependency)
    codeSemantic=summarizeSemantic(subCodesSemantics)
    return codeSemantic    

 

