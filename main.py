from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
import mysql.connector
from mysql.connector import Error

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ColoqueSuaSenhaAqui",
        database="hotel"
    )

class Cliente(BaseModel):
    descricao: str
    status: str
    check_in: date
    check_out: date
    quarto: int

@app.post("/clientes")
def criar_cliente(cliente: Cliente):

    try:
        conexao = conectar()

        cursor = conexao.cursor(dictionary=True)

        if cliente.quarto < 0 or cliente.quarto > 100:

            raise HTTPException(
                status_code=400,
                detail="Quarto deve estar entre 0 e 100"
            )

        if cliente.check_out <= cliente.check_in:

            raise HTTPException(
                status_code=400,
                detail="Check-out deve ser após check-in"
            )

        status_validos = [
            "ocupado",
            "livre",
            "reservado"
        ]

        if cliente.status.lower() not in status_validos:

            raise HTTPException(
                status_code=400,
                detail="Status inválido"
            )

        cursor.execute("""
            SELECT * FROM clientes
            WHERE quarto = %s
            AND (
                (%s BETWEEN check_in AND check_out)
                OR
                (%s BETWEEN check_in AND check_out)
                OR
                (check_in BETWEEN %s AND %s)
            )
        """, (
            cliente.quarto,

            cliente.check_in,

            cliente.check_out,

            cliente.check_in,
            cliente.check_out
        ))

        conflito = cursor.fetchone()

        if conflito:

            raise HTTPException(
                status_code=400,
                detail="Quarto já reservado/ocupado nesse período"
            )

        sql = """
            INSERT INTO clientes
            (
                descricao,
                status,
                check_in,
                check_out,
                quarto
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            cliente.descricao,
            cliente.status,
            cliente.check_in,
            cliente.check_out,
            cliente.quarto
        )

        cursor.execute(sql, valores)

        conexao.commit()

        return {
            "message": "Cliente cadastrado"
        }

    except Error as erro:

        raise HTTPException(
            status_code=500,
            detail=str(erro)
        )

    finally:

        if conexao.is_connected():
            cursor.close()
            conexao.close()

@app.get("/clientes")
def listar_clientes():

    try:
        conexao = conectar()

        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM clientes
            ORDER BY check_in ASC
        """)

        clientes = cursor.fetchall()

        return clientes

    finally:

        if conexao.is_connected():
            cursor.close()
            conexao.close()

@app.delete("/clientes/{id}")
def deletar_cliente(id: int):

    try:
        conexao = conectar()

        cursor = conexao.cursor()

        cursor.execute(
            "DELETE FROM clientes WHERE id = %s",
            (id,)
        )

        conexao.commit()

        return {
            "message": "Cliente removido"
        }

    finally:

        if conexao.is_connected():
            cursor.close()
            conexao.close()