# project.py
import whatif

def run_optimization(sql_query, what_if_questions):
    """
    Main function to run the query optimization based on what-if questions.
    """
    what_if_modifications = [{"change": q} for q in what_if_questions]
    result = whatif.generate_aqp(sql_query, what_if_modifications)

    # Format output
    output = (
        f"Original SQL Query:\n{result['original_sql']}\n\n"
        f"Modified SQL Query:\n{result['modified_sql']}\n\n"
        f"Original Query Plan and Cost:\n{result['original_plan']} | Cost: {result['original_cost']}\n\n"
        f"Modified Query Plan (AQP) and Cost:\n{result['modified_plan']} | Cost: {result['modified_cost']}"
    )
    return output

if __name__ == "__main__":
    # Example SQL query and what-if questions
    sql_query = "SELECT * FROM employees WHERE age > 30;"
    what_if_questions = ["change join order", "use index on age"]

    print(run_optimization(sql_query, what_if_questions))
