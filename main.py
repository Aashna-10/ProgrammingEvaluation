from openai import OpenAI
def get_completion(prompt):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    )
    return (completion.choices[0].message.content)
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
        if SCDepth<threshold:
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

